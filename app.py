import streamlit as st

from utils import load_csv

# ---------- Page setup ----------
st.set_page_config(
    page_title="Search engine", page_icon=":material/search:", layout="wide"
)

# ---------- Sidebar: Upload & Options ----------
st.sidebar.caption("Welcome to the search engine")
st.sidebar.header("Upload CSV")
file = st.sidebar.file_uploader(
    "Upload a CSV file with one **rghc** column and one **full_text** column",
    type=["csv"],
    accept_multiple_files=False,
)

if file is not None:
    df = load_csv(file.getvalue())
    st.sidebar.success(f"Loaded {len(df):,} rows × {len(df.columns)} columns")

    # Fixed column names per user request
    id_col = "rghc"
    text_col = "full_text"

    if id_col not in df.columns or text_col not in df.columns:
        st.error(
            f"CSV must contain columns '{id_col}' and '{text_col}'. Found: {', '.join(df.columns)}"
        )
        st.stop()

    # persist data storage for other pages
    st.session_state["data"] = {"df": df, "id_col": id_col, "text_col": text_col}

global_page = st.Page(
    "pages/global.py", title="Search through all records", icon=":material/search:"
)
patient_page = st.Page(
    "pages/patient.py",
    title="Search a given rghc record",
    icon=":material/saved_search:",
)

tazi_page = st.Page(
    "pages/tazi_ui.py",
    title="Consult Tazi Records",
    icon=":material/deployed_code_account:",
)

pg = st.navigation([global_page, patient_page, tazi_page])
pg.run()
