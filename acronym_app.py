import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Internal Acronym Dictionary",
    page_icon="📘",
    layout="centered"
)

# -----------------------------
# SIMPLE LOGIN (ONE USER)
# -----------------------------
USERNAME = "unilever"
PASSWORD = "innovation2026"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 Internal Access")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == USERNAME and pwd == PASSWORD:
            st.session_state["authenticated"] = True
            st.success("Access granted")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel(
        "Unilever Acronym List - Multiple Lookup (1).xlsx",
        sheet_name=0,
        engine="openpyxl"
    )
    df.columns = [c.strip() for c in df.columns]
    df = df.iloc[:, :2]
    df.columns = ["Acronym", "Definition"]
    df["Acronym"] = df["Acronym"].astype(str).str.strip()
    df["Definition"] = df["Definition"].astype(str).str.strip()
    return df.dropna()

@st.cache_data(ttl=0)
def load_data():
    df = pd.read_excel(
        "Unilever Acronym List - Multiple Lookup (1).xlsx",
        sheet_name=0,
        engine="openpyxl"
    )

    # Keep only first two columns
    df = df.iloc[:, :2]
    df.columns = ["Acronym", "Definition"]

    # Strong cleaning (THIS IS THE KEY)
    df["Acronym"] = (
        df["Acronym"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["Definition"] = (
        df["Definition"]
        .astype(str)
        .str.strip()
    )

    return df.dropna()


if search:
    results = df["Acronym"].str.contains(search.strip().upper(), nan=False)
    if results.empty:
        st.warning("No results found.")
    else:
        st.dataframe(results, use_container_width=True)
