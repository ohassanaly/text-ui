import streamlit as st

from utils import load_csv

# ---------- Page setup ----------
st.set_page_config(page_title="EMR-UI", page_icon=":material/search:", layout="wide")

# ---------- Sidebar: Upload & Options ----------
st.sidebar.caption("Welcome to the Electronic Medical Records User Interface (EMR-UI)")
st.sidebar.caption(
    "You can use either built-in modules (Tasy and HCMed) or custom search"
)
st.sidebar.header("Custom search : Upload CSV")
file = st.sidebar.file_uploader(
    "Upload a CSV file with one **rghc** column, one **data** column and one **full_text** column",
    type=["csv"],
    accept_multiple_files=False,
)

if file is not None:
    df = load_csv(file.getvalue())
    st.sidebar.success(f"Loaded {len(df):,} rows × {len(df.columns)} columns")

    # Fixed column names per user request
    id_col = "rghc"
    text_col = "full_text"
    date_col = "data"

    if (
        id_col not in df.columns
        or text_col not in df.columns
        or date_col not in df.columns
    ):
        st.error(
            f"CSV must contain columns '{id_col}' and '{text_col}' and '{date_col}'. Found: {', '.join(df.columns)}"
        )
        st.stop()

    # persist data storage for other pages
    st.session_state["data"] = {
        "df": df,
        "id_col": id_col,
        "text_col": text_col,
        "date_col": date_col,
    }

global_page = st.Page(
    "pages/global.py", title="Search through all records", icon=":material/search:"
)
patient_page = st.Page(
    "pages/patient.py",
    title="Search a given record",
    icon=":material/saved_search:",
)

tasy_page = st.Page(
    "pages/tasy_ui_fuzzy.py",
    title="Consult Tasy Records",
    icon=":material/deployed_code_account:",
)

exam_page = st.Page(
    "pages/exams.py",
    title="Retrieve HCMed lab exams",
    icon=":material/heart_plus:",
)

redcap_page = st.Page(
    "pages/redcap_ui.py",
    title="Search with Redcap API",
    icon=":material/data_check:",
)

full_tasy_page = st.Page(
    "pages/full_tasy_ui.py",
    title="Datalake UI",
    icon=":material/dataset:",
)


pg = st.navigation(
    [global_page, patient_page, tasy_page, exam_page, redcap_page, full_tasy_page]
)
pg.run()
