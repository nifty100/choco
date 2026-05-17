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
    page_title="NSE Historical Option Downloader",
    layout="wide"
)

st.title("NSE Historical Option Data Downloader")

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
    value=10300,
    step=50
)

option_type = st.selectbox(
    "Option Type",
    ["CE", "PE"]
)

from_date = st.date_input(
    "From Date",
    value=datetime(2020, 6, 1)
)

to_date = st.date_input(
    "To Date",
    value=datetime(2020, 6, 30)
)

# ---------------------------------------------------
# FETCH FUNCTION
# ---------------------------------------------------

def fetch_data():

    final_data = []

    current_date = from_date

    while current_date <= to_date:

        # Skip weekends
        if current_date.weekday() >= 5:
            current_date += timedelta(days=1)
            continue

        day = current_date.strftime("%d")
        month = current_date.strftime("%b").upper()
        year = current_date.strftime("%Y")

        zip_file_name = (
            f"fo{day}{month}{year}bhav.csv.zip"
        )

        url = (
            "https://archives.nseindia.com/content/"
            "historical/DERIVATIVES/"
            f"{year}/{month}/{zip_file_name}"
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

            csv_name = zip_file.namelist()[0]

            df = pd.read_csv(
                zip_file.open(csv_name)
            )

            # -----------------------------------------
            # FILTER
            # -----------------------------------------

            filtered = df[
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
                    == "OPTIDX"
                )
            ]

            if not filtered.empty:

                for _, row in filtered.iterrows():

                    clean_row = {

                        "Symbol":
                        row["SYMBOL"],

                        "Date":
                        row["TIMESTAMP"],

                        "Expiry":
                        row["EXPIRY_DT"],

                        "Option type":
                        row["OPTION_TYP"],

                        "Strike Price":
                        row["STRIKE_PR"],

                        "Open":
                        row["OPEN"],

                        "High":
                        row["HIGH"],

                        "Low":
                        row["LOW"],

                        "Close":
                        row["CLOSE"],

                        "LTP":
                        row["CLOSE"],

                        "Settle Price":
                        row["SETTLE_PR"],

                        "No. of contracts":
                        row["CONTRACTS"],

                        "Turnover * in ₹ Lakhs":
                        row["VAL_INLAKH"],

                        "Premium Turnover ** in ₹ Lakhs":
                        row["VAL_INLAKH"],

                        "Open Int":
                        row["OPEN_INT"],

                        "Change in OI":
                        row["CHG_IN_OI"],

                        "Underlying Value":
                        row["CLOSE"]
                    }

                    final_data.append(clean_row)

        except:
            pass

        current_date += timedelta(days=1)

    return pd.DataFrame(final_data)

# ---------------------------------------------------
# BUTTON
# ---------------------------------------------------

if st.button("Fetch Option Data"):

    try:

        with st.spinner(
            "Fetching historical option data..."
        ):

            final_df = fetch_data()

        if final_df.empty:

            st.warning(
                "No matching data found."
            )

        else:

            # -----------------------------------------
            # SORT BY DATE
            # -----------------------------------------

            final_df["Date"] = pd.to_datetime(
                final_df["Date"]
            )

            final_df = final_df.sort_values(
                by="Date",
                ascending=False
            )

            # -----------------------------------------
            # DATE FORMAT
            # -----------------------------------------

            final_df["Date"] = (
                final_df["Date"]
                .dt.strftime("%d-%b-%Y")
            )

            # -----------------------------------------
            # DISPLAY
            # -----------------------------------------

            st.success(
                f"{len(final_df)} rows fetched."
            )

            st.dataframe(final_df)

            # -----------------------------------------
            # FILE NAME
            # -----------------------------------------

            filename = (
                f"OPTIDX_"
                f"{symbol}_"
                f"{option_type}_"
                f"{from_date.strftime('%d-%b-%Y')}"
                f"_TO_"
                f"{to_date.strftime('%d-%b-%Y')}.csv"
            )

            # -----------------------------------------
            # DOWNLOAD
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
