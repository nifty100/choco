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
# FETCH FUNCTION
# ---------------------------------------------------

def fetch_bhavcopy_data():

    final_df = []

    current_date = from_date

    while current_date <= to_date:

        # Skip weekends
        if current_date.weekday() >= 5:
            current_date += timedelta(days=1)
            continue

        day = current_date.strftime("%d")
        month = current_date.strftime("%b").upper()
        year = current_date.strftime("%Y")

        # Example URL:
        # https://archives.nseindia.com/content/historical/DERIVATIVES/2022/DEC/fo01DEC2022bhav.csv.zip

        zip_filename = (
            f"fo{day}{month}{year}bhav.csv.zip"
        )

        url = (
            "https://archives.nseindia.com/content/"
            f"historical/DERIVATIVES/"
            f"{year}/{month}/{zip_filename}"
        )

        try:

            response = requests.get(
                url,
                timeout=20
            )

            if response.status_code != 200:
                current_date += timedelta(days=1)
                continue

            # -----------------------------------------
            # READ ZIP
            # -----------------------------------------

            zip_file = zipfile.ZipFile(
                io.BytesIO(response.content)
            )

            csv_file = zip_file.namelist()[0]

            df = pd.read_csv(
                zip_file.open(csv_file)
            )

            # -----------------------------------------
            # STRICT FILTERS
            # -----------------------------------------

            filtered_df = df[
                (
                    df["SYMBOL"]
                    .astype(str)
                    .str.upper()
                    == symbol
                )
                &
                (
                    df["STRIKE_PR"]
                    == strike_price
                )
                &
                (
                    df["OPTION_TYP"]
                    .astype(str)
                    .str.upper()
                    == option_type
                )
                &
                (
                    df["INSTRUMENT"]
                    .isin(["OPTIDX", "OPTSTK"])
                )
            ]

            # -----------------------------------------
            # ADD ONLY MATCHING ROWS
            # -----------------------------------------

            if not filtered_df.empty:

                final_df.append(filtered_df)

        except:
            pass

        current_date += timedelta(days=1)

    # -----------------------------------------
    # COMBINE DATA
    # -----------------------------------------

    if len(final_df) == 0:
        return pd.DataFrame()

    combined_df = pd.concat(
        final_df,
        ignore_index=True
    )

    return combined_df

# ---------------------------------------------------
# FETCH BUTTON
# ---------------------------------------------------

if st.button("Fetch Option Data"):

    try:

        with st.spinner(
            "Fetching filtered option data..."
        ):

            final_df = fetch_bhavcopy_data()

        if final_df.empty:

            st.warning(
                "No matching data found."
            )

        else:

            st.success(
                f"{len(final_df)} matching rows fetched."
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
            # DOWNLOAD CSV
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
