import streamlit as st
import pandas as pd
import re

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
# LOAD DATA (SAFE FOR REAL EXCEL)
# -----------------------------
@st.cache_data
def load_data():
    excel_file = "Unilever Acronym List - Multiple Lookup (1).xlsx"
    xls = pd.ExcelFile(excel_file, engine="openpyxl")

    rows = []

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, header=None)

        for _, row in df.iterrows():
            values = [str(v).strip() for v in row if pd.notna(v)]

            if len(values) < 2:
                continue

            acronym = values[0].upper()
            definition = values[1]

            # ✅ VALIDATE ACRONYM SHAPE (KEY FIX)
            if re.fullmatch(r"[A-Z0-9/&\-]{2,10}", acronym):
                rows.append(
                    {"Acronym": acronym, "Definition": definition}
                )

    return pd.DataFrame(rows)

# -----------------------------
# REFRESH BUTTON
# -----------------------------
st.sidebar.title("Admin")
if st.sidebar.button("🔄 Refresh data"):
    st.cache_data.clear()
    st.rerun()

df = load_data()

# -----------------------------
# APP UI
# -----------------------------
st.title("📘 Acronym Dictionary")
st.write("Internal reference tool for acronym definitions.")

search = st.text_input("Enter an acronym (e.g. POP, MPT, FDTC):")

if search:
    results = df[df["Acronym"].str.contains(search.strip().upper(), na=False)]

    if results.empty:
        st.warning("No results found.")
    else:
        st.dataframe(results, use_container_width=True)
