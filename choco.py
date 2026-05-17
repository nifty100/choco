import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ---------------------------------------------------
# STREAMLIT PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Option Data Downloader",
    layout="wide"
)

st.title("Historical Option Data Downloader")

st.write(
    "Fetch historical option data using Upstox API "
    "and download filtered CSV."
)

# ---------------------------------------------------
# USER INPUTS
# ---------------------------------------------------

access_token = st.text_input(
    "Enter Upstox Access Token",
    type="password"
)

symbol = st.text_input(
    "Symbol",
    value="NIFTY"
).upper()

expiry = st.text_input(
    "Expiry Date (Example: 2022-12-29)",
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
# FETCH FUNCTION
# ---------------------------------------------------

def fetch_option_data():

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    # ---------------------------------------------
    # STEP 1: SEARCH INSTRUMENT
    # ---------------------------------------------

    instrument_url = (
        "https://api.upstox.com/v2/option/contract"
    )

    params = {
        "instrument_key": f"NSE_INDEX|{symbol}",
        "expiry_date": expiry
    }

    response = requests.get(
        instrument_url,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        raise Exception(
            f"Instrument Fetch Error: "
            f"{response.status_code}"
        )

    instrument_data = response.json()

    if "data" not in instrument_data:
        raise Exception(
            "No instrument data found."
        )

    contracts = instrument_data["data"]

    matched_contract = None

    for item in contracts:

        strike_match = (
            float(item.get("strike_price", 0))
            == float(strike_price)
        )

        option_match = (
            item.get("option_type", "")
            .upper()
            == option_type
        )

        if strike_match and option_match:
            matched_contract = item
            break

    if matched_contract is None:
        raise Exception(
            "Matching option contract not found."
        )

    instrument_key = matched_contract[
        "instrument_key"
    ]

    # ---------------------------------------------
    # STEP 2: FETCH HISTORICAL DATA
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
            f"Historical Data Error: "
            f"{historical_response.status_code}"
        )

    historical_data = historical_response.json()

    if "data" not in historical_data:
        raise Exception(
            "No historical data found."
        )

    candles = historical_data["data"].get(
        "candles",
        []
    )

    if len(candles) == 0:
        raise Exception(
            "No candle data available."
        )

    # ---------------------------------------------
    # CREATE DATAFRAME
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
            "OI"
        ]
    )

    return df

# ---------------------------------------------------
# BUTTON ACTION
# ---------------------------------------------------

if st.button("Fetch Data"):

    try:

        if access_token.strip() == "":
            st.error(
                "Please enter Upstox Access Token."
            )

        else:

            with st.spinner(
                "Fetching historical data..."
            ):

                df = fetch_option_data()

            st.success(
                f"{len(df)} rows fetched successfully."
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
            # DOWNLOAD CSV
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
