import json

import streamlit as st

from utils import (
    escape_markdown,
    highlight_html_fuzzy,
    normalize_text,
    retrieve_context_fuzzy,
)

st.caption(
    "Here the data is loaded from the data folder ; you don't need to upload anything"
)

with open("data/tasy_records.json", "r") as f:
    json_data = json.load(f)

with st.form("Tasy fuzzy search"):
    rghc = st.text_input("rghc", placeholder="Enter a rghc to access its record")
    word_query = st.text_input(
        "ex : recaida", placeholder="Enter your search query (optional)"
    )
    l_dist = st.number_input(
        "Levenshtein distance: set 0 for an exact search",
        min_value=0,
        value=1,
        max_value=3,
        step=1,
        format="%d",
    )

    submit_search = st.form_submit_button("Search")

    if submit_search:
        if rghc in list(json_data.keys()):
            record = json_data[rghc]

            if word_query:
                full_text = normalize_text("\n".join(record.values())).strip()
                matches = retrieve_context_fuzzy(word_query, full_text, l_dist)
                if matches:
                    st.subheader(f"{len(matches)} matches found")
                    st.markdown(
                        "\n\n".join(
                            [
                                highlight_html_fuzzy(
                                    word_query, escape_markdown(m), l_dist
                                )
                                for m in matches
                            ]
                        ),
                        unsafe_allow_html=True,
                    )
                else:
                    st.info("No match found")
            st.subheader("Full record")
            st.json({k: v for k, v in record.items() if v != ""})

        else:
            st.info("invalid rghc")
