import streamlit as st

from utils import escape_markdown, highlight_html

if "data" not in st.session_state:
    st.warning("Please upload a CSV in the sidebar first")
    st.stop()

data = st.session_state["data"]
df = data["df"]
id_col = data["id_col"]
text_col = data["text_col"]

# Search controls
st.header("Search for a specific rghc")
id_query = st.text_input("any rghc", placeholder="Enter rghc")

if not id_query:
    st.table(df[id_col])

if id_query:
    if id_query in df.rghc.tolist():
        word_query = st.text_input(
            "ex : recaida", placeholder="Enter your search query"
        )
        if word_query:
            text = df[df.rghc == id_query][text_col].squeeze()
            st.download_button(
                label="download full text",
                data=text.encode("utf-8"),
                file_name=f"{id_query}.txt",
                mime="text/plain",
            )
            if word_query not in text:
                st.info("No match found")
            st.markdown(
                highlight_html(word_query, escape_markdown(text)),
                unsafe_allow_html=True,
            )
        else:
            st.info("Enter a search query in the sidebar")
    else:
        st.info("Enter a valid rghc")

else:
    pass
