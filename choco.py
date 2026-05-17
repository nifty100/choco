import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from io import StringIO

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
    "Enter Symbol",
    value="NIFTY"
).upper()

strike_price = st.number_input(
    "Enter Strike Price",
    min_value=0,
    step=50,
    value=23000
)

option_type = st.selectbox(
    "Select Option Type",
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
# FETCH NSE DATA
# ---------------------------------

def fetch_nse_csv():

    # NSE historical derivatives CSV URL
    url = (
        "https://www.nseindia.com/api/"
        "historical/foCPV?"
        f"symbol={symbol}"
        "&instrumentType=OPTIDX"
        f"&from={from_date.strftime('%d-%m-%Y')}"
        f"&to={to_date.strftime('%d-%m-%Y')}"
    )

    session = requests.Session()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/",
        "Accept": "application/json"
    }

    # Get cookies first
    session.get(
        "https://www.nseindia.com",
        headers=headers
    )

    response = session.get(
        url,
        headers=headers
    )

    if response.status_code != 200:
        raise Exception(
            f"NSE API Error: {response.status_code}"
        )

    try:
        json_data = response.json()
    except Exception:
        raise Exception(
            "NSE did not return JSON data."
        )

    if "data" not in json_data:
        raise Exception(
            "No data field found in NSE response."
        )

    return pd.DataFrame(json_data["data"])

# ---------------------------------
# BUTTON ACTION
# ---------------------------------

if st.button("Fetch & Download CSV"):

    try:

        df = fetch_nse_csv()

        # ---------------------------------
        # FILTERS
        # ---------------------------------

        # Strike Filter
        if "strikePrice" in df.columns:
            df = df[
                df["strikePrice"] == strike_price
            ]

        # Option Type Filter
        if "optionType" in df.columns:
            df = df[
                df["optionType"]
                .astype(str)
                .str.upper() == option_type
            ]

        # ---------------------------------
        # FILE NAME
        # ---------------------------------

        from_str = pd.to_datetime(
            from_date
        ).strftime("%d-%b-%Y")

        to_str = pd.to_datetime(
            to_date
        ).strftime("%d-%b-%Y")

        filename = (
            f"{symbol}_"
            f"{strike_price}_"
            f"{option_type}_"
            f"{from_str}_TO_{to_str}.csv"
        )

        # ---------------------------------
        # DOWNLOAD
        # ---------------------------------

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.success(
            f"Rows Found: {len(df)}"
        )

        st.dataframe(df.head())

        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=filename,
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")
