import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import time

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="NSE Option Data Downloader",
    layout="centered"
)

st.title("NSE Option Data Downloader")

# ---------------------------------
# INPUTS
# ---------------------------------

symbol = st.text_input(
    "Symbol",
    value="NIFTY"
).upper()

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

# ---------------------------------
# NSE FETCH FUNCTION
# ---------------------------------

def get_nse_data():

    base_url = "https://www.nseindia.com/"

    api_url = (
        "https://www.nseindia.com/api/historical/foCPV?"
        f"symbol={symbol}"
        "&instrumentType=OPTIDX"
        f"&from={from_date.strftime('%d-%m-%Y')}"
        f"&to={to_date.strftime('%d-%m-%Y')}"
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/",
        "Connection": "keep-alive"
    }

    session = requests.Session()

    # Step 1: Visit NSE homepage first
    home_response = session.get(
        base_url,
        headers=headers,
        timeout=10
    )

    if home_response.status_code != 200:
        raise Exception(
            "Failed to connect to NSE homepage."
        )

    # Small delay helps bypass blocking
    time.sleep(1)

    # Step 2: Fetch API data
    response = session.get(
        api_url,
        headers=headers,
        timeout=20
    )

    if response.status_code != 200:
        raise Exception(
            f"NSE API Error: {response.status_code}"
        )

    # Debug output
    content_type = response.headers.get("Content-Type", "")

    if "json" not in content_type.lower():
        raise Exception(
            "NSE blocked the request or returned non-JSON response."
        )

    data = response.json()

    if "data" not in data:
        raise Exception(
            "No data found in NSE response."
        )

    return pd.DataFrame(data["data"])

# ---------------------------------
# BUTTON
# ---------------------------------

if st.button("Fetch Data"):

    try:

        df = get_nse_data()

        # ---------------------------------
        # FILTER DATA
        # ---------------------------------

        if "strikePrice" in df.columns:
            df = df[
                df["strikePrice"] == strike_price
            ]

        if "optionType" in df.columns:
            df = df[
                df["optionType"]
                .astype(str)
                .str.upper() == option_type
            ]

        # ---------------------------------
        # FILE NAME
        # ---------------------------------

        from_str = from_date.strftime("%d-%b-%Y")
        to_str = to_date.strftime("%d-%b-%Y")

        filename = (
            f"{symbol}_"
            f"{strike_price}_"
            f"{option_type}_"
            f"{from_str}_TO_{to_str}.csv"
        )

        # ---------------------------------
        # DOWNLOAD CSV
        # ---------------------------------

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.success(
            f"{len(df)} rows fetched successfully."
        )

        st.dataframe(df.head())

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=filename,
            mime="text/csv"
        )

    except Exception as e:
        st.error(str(e))
