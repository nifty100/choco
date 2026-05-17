import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Yahoo Finance Option Downloader",
    layout="wide"
)

st.title("Yahoo Finance Option Data Downloader")

st.write(
    "Download historical option data using Yahoo Finance"
)

# ---------------------------------------------------
# USER INPUTS
# ---------------------------------------------------

symbol = st.text_input(
    "Enter Yahoo Finance Symbol",
    value="^NSEI"
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
# FETCH OPTION DATA
# ---------------------------------------------------

def fetch_option_data():

    ticker = yf.Ticker(symbol)

    # ---------------------------------------------
    # GET OPTION CHAIN
    # ---------------------------------------------

    option_chain = ticker.option_chain(expiry)

    if option_type == "CE":
        df = option_chain.calls
    else:
        df = option_chain.puts

    # ---------------------------------------------
    # FILTER STRIKE PRICE
    # ---------------------------------------------

    df = df[
        df["strike"] == strike_price
    ]

    if df.empty:
        raise Exception(
            "No option data found for selected strike."
        )

    # ---------------------------------------------
    # DATE FILTER
    # ---------------------------------------------

    if "lastTradeDate" in df.columns:

        df["lastTradeDate"] = pd.to_datetime(
            df["lastTradeDate"]
        )

        df = df[
            (
                df["lastTradeDate"]
                >= pd.to_datetime(from_date)
            )
            &
            (
                df["lastTradeDate"]
                <= pd.to_datetime(to_date)
            )
        ]

    if df.empty:
        raise Exception(
            "No data found within selected dates."
        )

    return df

# ---------------------------------------------------
# FETCH BUTTON
# ---------------------------------------------------

if st.button("Fetch Option Data"):

    try:

        with st.spinner(
            "Fetching option data..."
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
