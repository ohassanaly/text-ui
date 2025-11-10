import streamlit as st
from fuzzysearch import find_near_matches

from utils import escape_markdown, highlight_html_fuzzy

if "data" not in st.session_state:
    st.warning("Please upload a CSV in the sidebar first")
    st.stop()

data = st.session_state["data"]
df = data["df"]
id_col = data["id_col"]
text_col = data["text_col"]
date_col = data["date_col"]

# Search controls
st.header("Search for a specific rghc")
id_query = st.text_input("any rghc", placeholder="Enter rghc")
l_dist = st.number_input(
    "Levenshtein distance : set 0 for an exact search",
    min_value=0,
    value=1,
    max_value=3,
    step=1,
    format="%d",
)

if not id_query:
    st.table(df[id_col])

if id_query:
    if id_query in df.rghc.tolist():
        word_query = st.text_input(
            "ex : recaida", placeholder="Enter your search query"
        )
        if word_query:
            text = df[df.rghc == id_query][text_col].squeeze()
            date = df[df.rghc == id_query][date_col].squeeze()
            st.markdown(f"**Record date: {date}**")
            st.download_button(
                label="download full text",
                data=text.encode("utf-8"),
                file_name=f"{id_query}.txt",
                mime="text/plain",
            )
            matches = find_near_matches(word_query, text, max_l_dist=l_dist)
            if word_query not in text:
                st.info("No match found")
            st.markdown(
                highlight_html_fuzzy(word_query, escape_markdown(text), l_dist),
                unsafe_allow_html=True,
            )
        else:
            st.info("Enter a search query in the sidebar")
    else:
        st.info("Enter a valid rghc")

else:
    pass
