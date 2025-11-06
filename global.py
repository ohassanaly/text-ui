import streamlit as st

from utils import escape_markdown, highlight_html, retrieve_context, text_search

if "data" not in st.session_state:
    st.warning("Please upload a CSV in the sidebar first")
    st.stop()

data = st.session_state["data"]
df = data["df"]
id_col = data["id_col"]
text_col = data["text_col"]

# Search controls
st.header(f"Search words through all the {df.rghc.nunique()} records")
query = st.text_input("ex : recaida", placeholder="Enter your search query")

if query:
    res_df = text_search(query, df, "full_text")
    if res_df.empty:
        st.warning("No matches found.")
    else:
        st.info(
            f"{res_df.rghc.nunique()} / {df.rghc.nunique()}  rghc match the search query"
        )
    for index, row in res_df.iterrows():
        st.markdown(f"**rghc: {row[id_col]}**")
        with st.expander("show context of the match(es)"):
            st.download_button(
                label="download full text",
                data=row[text_col].encode("utf-8"),
                file_name=f"{row[id_col]}.txt",
                mime="text/plain",
            )
            matches = retrieve_context(query, row[text_col])
            st.markdown(
                "\n\n".join(
                    [highlight_html(query, escape_markdown(m)) for m in matches]
                ),
                unsafe_allow_html=True,
            )
else:
    st.info(
        f"Enter a search query in the sidebar to look for matches in all the database ({df.rghc.nunique()} available patient records)"
    )
