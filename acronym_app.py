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
# LOAD DATA FROM ALL SHEETS (ROBUST)
# -----------------------------
@st.cache_data
def load_data():
    excel_file = "Unilever Acronym List - Multiple Lookup (1).xlsx"
    xls = pd.ExcelFile(excel_file, engine="openpyxl")

    all_rows = []

    for sheet in xls.sheet_names:
        raw = pd.read_excel(xls, sheet_name=sheet, header=None)

