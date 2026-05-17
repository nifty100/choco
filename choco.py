import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from io import BytesIO

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="NSE Option CSV Downloader",
    layout="centered"
)

st.title("NSE Option CSV Downloader")

# ---------------------------------
# USER INPUTS
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
# FETCH FUNCTION
# ---------------------------------

def fetch_data():

    url = (
        "https://www.nseindia.com/api/"
        "historical/fo/derivatives"
    )

    params = {
        "from": from_date.strftime("%d-%m-%Y"),
        "to": to_date.strftime("%d-%m-%Y"),
        "instrumentType": "OPTIDX",
        "symbol": symbol
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com/",
        "Origin": "https://www.nseindia.com"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(
            f"NSE API Error: {response.status_code}"
        )

    try:
        data = response.json()
    except:
        raise Exception(
            "NSE blocked request or returned invalid data."
        )

    if "data" not in data:
        raise Exception(
            "No data found."
        )

    return pd.DataFrame(data["data"])

# ---------------------------------
# BUTTON
# ---------------------------------

if st.button("Fetch Data"):

    try:

        df = fetch_data()

        # ---------------------------------
        # FILTERS
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
        # EMPTY CHECK
        # ---------------------------------

        if len(df) == 0:
            st.warning(
                "No matching data found."
            )
        else:

            st.success(
                f"{len(df)} rows fetched."
            )

            st.dataframe(df.head())

            # ---------------------------------
            # FILE NAME
            # ---------------------------------

            from_str = from_date.strftime(
                "%d-%b-%Y"
            )

            to_str = to_date.strftime(
                "%d-%b-%Y"
            )

            filename = (
                f"{symbol}_"
                f"{strike_price}_"
                f"{option_type}_"
                f"{from_str}_TO_{to_str}.csv"
            )

            # ---------------------------------
            # DOWNLOAD
            # ---------------------------------

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
