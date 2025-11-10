import streamlit as st

from utils import (
    escape_markdown,
    highlight_html_fuzzy,
    retrieve_context_fuzzy,
    text_search_fuzzy,
)

if "data" not in st.session_state:
    st.warning("Please upload a CSV in the sidebar first")
    st.stop()

data = st.session_state["data"]
df = data["df"]
id_col = data["id_col"]
text_col = data["text_col"]
date_col = data["date_col"]

# Search controls
st.header(f"Search words through all the {df.rghc.nunique()} records")
query = st.text_input("ex : recaida", placeholder="Enter your search query")
l_dist = st.number_input(
    "Levenshtein distance : set 0 for an exact search",
    min_value=0,
    value=1,
    max_value=2,
    step=1,
    format="%d",
)

if query:
    res_df = text_search_fuzzy(query, df, "full_text", l_dist)
    if res_df.empty:
        st.warning("No matches found.")
    else:
        st.info(
            f"{res_df.rghc.nunique()} / {df.rghc.nunique()}  rghc match the search query"
        )
    for index, row in res_df.iterrows():
        st.markdown(f"**rghc: {row[id_col]}** ; **Record date: {row[date_col]}**")
        with st.expander("show context of the match(es)"):
            st.download_button(
                label="download full text",
                data=row[text_col].encode("utf-8"),
                file_name=f"{row[id_col]}.txt",
                mime="text/plain",
            )
            matches = retrieve_context_fuzzy(query, row[text_col], l_dist)
            st.markdown(
                "\n\n".join(
                    [
                        highlight_html_fuzzy(query, escape_markdown(m), l_dist)
                        for m in matches
                    ]
                ),
                unsafe_allow_html=True,
            )
else:
    st.info(
        f"Enter a search query in the sidebar to look for matches in all the database ({df.rghc.nunique()} available patient records)"
    )
