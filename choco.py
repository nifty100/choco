import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from io import StringIO

# ---------------------------------
# NSE Option Data Downloader
# ---------------------------------

st.set_page_config(
    page_title="NSE Option CSV Downloader",
    layout="centered"
)

st.title("NSE Option CSV Downloader")

st.write(
    "Download NSE option data filtered by "
    "Symbol, Strike Price, Option Type and Date Range."
)

# ---------------------------------
# User Inputs
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
# Fetch NSE CSV Data
# ---------------------------------

def fetch_nse_data():
    """
    Fetch CSV report from NSE
    """

    url = "https://www.nseindia.com/report-detail/fo_eq_security"

    session = requests.Session()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/",
    }

    # Generate NSE cookies
    session.get(
        "https://www.nseindia.com",
        headers=headers
    )

    # Actual request
    response = session.get(
        url,
        headers=headers
    )

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch NSE data. "
            f"Status code: {response.status_code}"
        )

    return response.text


# ---------------------------------
# Download Logic
# ---------------------------------

if st.button("Fetch & Download CSV"):

    try:

        csv_text = fetch_nse_data()

        df = pd.read_csv(StringIO(csv_text))

        # ---------------------------------
        # Detect Important Columns
        # ---------------------------------

        possible_symbol_cols = [
            "SYMBOL",
            "Symbol"
        ]

        possible_date_cols = [
            "DATE",
            "Date",
            "TIMESTAMP"
        ]

        possible_strike_cols = [
            "STRIKE_PR",
            "STRIKE PRICE",
            "STRIKE_PRICE",
            "STRIKE"
        ]

        possible_option_cols = [
            "OPTION_TYP",
            "OPTION TYPE",
            "OPTION_TYPE"
        ]

        symbol_col = None
        date_col = None
        strike_col = None
        option_col = None

        for col in possible_symbol_cols:
            if col in df.columns:
                symbol_col = col
                break

        for col in possible_date_cols:
            if col in df.columns:
                date_col = col
                break

        for col in possible_strike_cols:
            if col in df.columns:
                strike_col = col
                break

        for col in possible_option_cols:
            if col in df.columns:
                option_col = col
                break

        # ---------------------------------
        # Apply Filters
        # ---------------------------------

        # Symbol Filter
        if symbol_col:
            df = df[
                df[symbol_col]
                .astype(str)
                .str.upper()
                == symbol
            ]

        # Date Filter
        if date_col:
            df[date_col] = pd.to_datetime(
                df[date_col],
                errors="coerce"
            )

            df = df[
                (df[date_col] >= pd.to_datetime(from_date))
                &
                (df[date_col] <= pd.to_datetime(to_date))
            ]

        # Strike Filter
        if strike_col:
            df = df[
                df[strike_col] == strike_price
            ]

        # Option Type Filter
        if option_col:
            df = df[
                df[option_col]
                .astype(str)
                .str.upper()
                == option_type
            ]

        # ---------------------------------
        # File Name
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
        # Download CSV
        # ---------------------------------

        csv_download = df.to_csv(
            index=False
        ).encode("utf-8")

        st.success(
            f"Filtered rows found: {len(df)}"
        )

        st.write("Preview:")

        st.dataframe(df.head())

        st.download_button(
            label="Download Filtered CSV",
            data=csv_download,
            file_name=filename,
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")
