import streamlit as st
import pandas as pd
import requests
import zipfile
import io
from datetime import datetime, timedelta

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="NSE Bhavcopy Option Downloader",
    layout="wide"
)

st.title("NSE Bhavcopy Option Data Downloader")

st.write(
    "Download historical NSE option data "
    "using NSE FO Bhavcopy archives."
)

# ---------------------------------------------------
# USER INPUTS
# ---------------------------------------------------

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

# ---------------------------------------------------
# NSE BHAVCOPY FETCH FUNCTION
# ---------------------------------------------------

def fetch_bhavcopy_data():

    final_df = pd.DataFrame()

    current_date = from_date

    while current_date <= to_date:

        # Skip weekends
        if current_date.weekday() >= 5:
            current_date += timedelta(days=1)
            continue

        day = current_date.strftime("%d")
        month = current_date.strftime("%b").upper()
        year = current_date.strftime("%Y")

        # Example:
        # https://archives.nseindia.com/content/historical/DERIVATIVES/2022/DEC/fo01DEC2022bhav.csv.zip

        file_name = (
            f"fo{day}{month}{year}bhav.csv.zip"
        )

        url = (
            "https://archives.nseindia.com/content/"
            f"historical/DERIVATIVES/"
            f"{year}/{month}/{file_name}"
        )

        try:

            response = requests.get(
                url,
                timeout=20
            )

            if response.status_code != 200:
                current_date += timedelta(days=1)
                continue

            zip_data = zipfile.ZipFile(
                io.BytesIO(response.content)
            )

            csv_name = zip_data.namelist()[0]

            df = pd.read_csv(
                zip_data.open(csv_name)
            )

            # -----------------------------------------
            # FILTERS
            # -----------------------------------------

            if "SYMBOL" in df.columns:

                df = df[
                    df["SYMBOL"]
                    .astype(str)
                    .str.upper() == symbol
                ]

            if "STRIKE_PR" in df.columns:

                df = df[
                    df["STRIKE_PR"]
                    == strike_price
                ]

            if "OPTION_TYP" in df.columns:

                df = df[
                    df["OPTION_TYP"]
                    .astype(str)
                    .str.upper() == option_type
                ]

            # Only Options
            if "INSTRUMENT" in df.columns:

                df = df[
                    df["INSTRUMENT"]
                    .isin(["OPTIDX", "OPTSTK"])
                ]

            final_df = pd.concat(
                [final_df, df],
                ignore_index=True
            )

        except:
            pass

        current_date += timedelta(days=1)

    return final_df

# ---------------------------------------------------
# FETCH BUTTON
# ---------------------------------------------------

if st.button("Fetch Option Data"):

    try:

        with st.spinner(
            "Downloading NSE Bhavcopy files..."
        ):

            final_df = fetch_bhavcopy_data()

        if final_df.empty:

            st.warning(
                "No matching option data found."
            )

        else:

            st.success(
                f"{len(final_df)} rows fetched."
            )

            st.dataframe(final_df)

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
            # CSV DOWNLOAD
            # -----------------------------------------

            csv = final_df.to_csv(
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
