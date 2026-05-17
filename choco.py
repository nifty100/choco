import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Historical Option Data Downloader",
    layout="wide"
)

st.title("Historical Option Data Downloader")

st.write(
    "Download historical option data using Upstox API"
)

# ---------------------------------------------------
# USER INPUTS
# ---------------------------------------------------

api_key = st.text_input(
    "Upstox API Key"
)

api_secret = st.text_input(
    "Upstox API Secret",
    type="password"
)

access_token = st.text_input(
    "Upstox Access Token",
    type="password"
)

symbol = st.text_input(
    "Symbol",
    value="NIFTY"
).upper()

expiry = st.text_input(
    "Expiry Date (YYYY-MM-DD)",
    value="2022-12-29"
)

strike_price = st.number_input(
    "Strike Price",
    min_value=0,
    value=23000,
    step=50
)

option_type = st.selectbox(
    "Option Type",
    ["CE", "PE"]
)

from_date = st.date_input(
    "From Date",
    value=datetime(2022, 12, 1)
)

to_date = st.date_input(
    "To Date",
    value=datetime(2022, 12, 31)
)

# ---------------------------------------------------
# SHOW LOGIN URL
# ---------------------------------------------------

if api_key != "":

    login_url = (
        "https://api-v2.upstox.com/login/"
        "authorization/dialog?"
        "response_type=code"
        f"&client_id={api_key}"
        "&redirect_uri=http://localhost"
    )

    st.markdown("### Step 1: Login URL")

    st.code(login_url)

    st.info(
        "Open this URL in browser, login and "
        "copy the code from redirected URL."
    )

# ---------------------------------------------------
# AUTH CODE INPUT
# ---------------------------------------------------

auth_code = st.text_input(
    "Paste Authorization Code Here"
)

# ---------------------------------------------------
# GENERATE ACCESS TOKEN
# ---------------------------------------------------

if st.button("Generate Access Token"):

    try:

        token_url = (
            "https://api-v2.upstox.com/login/"
            "authorization/token"
        )

        headers = {
            "accept": "application/json",
            "Api-Version": "2.0",
            "Content-Type":
            "application/x-www-form-urlencoded"
        }

        payload = {
            "code": auth_code,
            "client_id": api_key,
            "client_secret": api_secret,
            "redirect_uri": "http://localhost",
            "grant_type": "authorization_code"
        }

        response = requests.post(
            token_url,
            headers=headers,
            data=payload
        )

        data = response.json()

        generated_token = data.get(
            "access_token"
        )

        if generated_token:

            st.success(
                "Access Token Generated Successfully"
            )

            st.code(generated_token)

        else:

            st.error(data)

    except Exception as e:

        st.error(str(e))

# ---------------------------------------------------
# FETCH OPTION DATA FUNCTION
# ---------------------------------------------------

def fetch_option_data():

    headers = {
        "Accept": "application/json",
        "Authorization":
        f"Bearer {access_token}"
    }

    # ---------------------------------------------
    # FETCH OPTION CONTRACTS
    # ---------------------------------------------

    contract_url = (
        "https://api.upstox.com/v2/"
        "option/contract"
    )

    params = {
        "instrument_key":
        f"NSE_INDEX|{symbol}",
        "expiry_date": expiry
    }

    response = requests.get(
        contract_url,
        headers=headers,
        params=params
    )

    if response.status_code != 200:

        raise Exception(
            f"Contract API Error: "
            f"{response.status_code}"
        )

    contract_data = response.json()

    contracts = contract_data.get(
        "data",
        []
    )

    if len(contracts) == 0:

        raise Exception(
            "No option contracts found."
        )

    matched_contract = None

    for contract in contracts:

        strike_match = (
            float(contract.get(
                "strike_price",
                0
            )) == float(strike_price)
        )

        option_match = (
            contract.get(
                "option_type",
                ""
            ).upper() == option_type
        )

        if strike_match and option_match:

            matched_contract = contract
            break

    if matched_contract is None:

        raise Exception(
            "Matching option contract not found."
        )

    instrument_key = matched_contract[
        "instrument_key"
    ]

    # ---------------------------------------------
    # FETCH HISTORICAL DATA
    # ---------------------------------------------

    historical_url = (
        "https://api.upstox.com/v2/"
        "historical-candle/"
        f"{instrument_key}/day/"
        f"{to_date.strftime('%Y-%m-%d')}/"
        f"{from_date.strftime('%Y-%m-%d')}"
    )

    historical_response = requests.get(
        historical_url,
        headers=headers
    )

    if historical_response.status_code != 200:

        raise Exception(
            f"Historical API Error: "
            f"{historical_response.status_code}"
        )

    historical_data = (
        historical_response.json()
    )

    candles = historical_data.get(
        "data",
        {}
    ).get(
        "candles",
        []
    )

    if len(candles) == 0:

        raise Exception(
            "No historical candle data found."
        )

    # ---------------------------------------------
    # DATAFRAME
    # ---------------------------------------------

    df = pd.DataFrame(
        candles,
        columns=[
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "OpenInterest"
        ]
    )

    return df

# ---------------------------------------------------
# FETCH BUTTON
# ---------------------------------------------------

if st.button("Fetch Historical Data"):

    try:

        if access_token == "":

            st.error(
                "Please enter Access Token"
            )

        else:

            with st.spinner(
                "Fetching historical data..."
            ):

                df = fetch_option_data()

            st.success(
                f"{len(df)} rows fetched."
            )

            st.dataframe(df)

            # -----------------------------------------
            # FILE NAME
            # -----------------------------------------

            filename = (
                f"{symbol}_"
                f"{strike_price}_"
                f"{option_type}_"
                f"{from_date.strftime('%d-%b-%Y')}"
                f"_TO_"
                f"{to_date.strftime('%d-%b-%Y')}.csv"
            )

            # -----------------------------------------
            # DOWNLOAD BUTTON
            # -----------------------------------------

            csv = df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=filename,
                mime="text/csv"
            )

    except Exception as e:

        st.error(str(e))
