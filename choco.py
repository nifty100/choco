import streamlit as st
import pandas as pd
from datetime import datetime
from nsepython import *

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

def fetch_option_data():

    from_str = from_date.strftime("%d-%m-%Y")
    to_str = to_date.strftime("%d-%m-%Y")

    # NSE Historical Options Data
    data = nsefetch(
        f"https://www.nseindia.com/api/"
        f"historical/foCPV?"
        f"symbol={symbol}"
        f"&from={from_str}"
        f"&to={to_str}"
        f"&instrumentType=OPTIDX"
    )

    if "data" not in data:
        raise Exception("No data returned from NSE")

    df = pd.DataFrame(data["data"])

    return df

# ---------------------------------
# BUTTON
# ---------------------------------

if st.button("Fetch Data"):

    try:

        df = fetch_option_data()

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
            st.warning("No matching data found.")
        else:

            st.success(
                f"{len(df)} rows fetched successfully."
            )

            st.dataframe(df.head())

            # ---------------------------------
            # FILE NAME
            # ---------------------------------

            filename = (
                f"{symbol}_"
                f"{strike_price}_"
                f"{option_type}_"
                f"{from_date.strftime('%d-%b-%Y')}"
                f"_TO_"
                f"{to_date.strftime('%d-%b-%Y')}.csv"
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
