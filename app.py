from utils import load_csv, text_search, retrieve_context, highlight_html, escape_markdown
import pandas as pd
import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="motor de busca", page_icon="🔎", layout="wide")
st.title("🔎 Motor de busca")
st.caption("Upload a CSV with one **rghc** column and one **full_text** column")

# ---------- Sidebar: Upload & Options ----------
st.sidebar.header("1) Upload CSV")
file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"], accept_multiple_files=False)

if file is not None:
    df = load_csv(file.getvalue())
    st.sidebar.success(f"Loaded {len(df):,} rows × {len(df.columns)} columns")

    # Fixed column names per user request
    id_col = "rghc"
    text_col = "full_text"

    if id_col not in df.columns or text_col not in df.columns:
        st.error(f"CSV must contain columns '{id_col}' and '{text_col}'. Found: {', '.join(df.columns)}")
        st.stop()

    # Search controls
    st.sidebar.header("2) Search options")
    query = st.sidebar.text_input("Find", placeholder="your search")
    
    if query:
        res_df = text_search(query, df, "full_text")
        if res_df.empty:
            st.warning("No matches found.")
        else :
            st.info(f"{res_df.rghc.nunique()}, rghc found")
        for index, row in res_df.iterrows() :
            st.markdown(f"**rghc: {row[id_col]}**")
            with st.expander("show context of the matches"):
                st.download_button(label = "download full text", 
                                   data = row[text_col].encode("utf-8"), 
                                   file_name = f"{row[id_col]}.txt",
                                   mime="text/plain"
                                   )
                matches = retrieve_context(query, row[text_col])
                st.markdown("\n\n".join([highlight_html(query, escape_markdown(m)) for m in matches]), unsafe_allow_html=True)
    else:
        st.info("Enter a search query in the sidebar to begin.")
    