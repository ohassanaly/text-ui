import json

import pandas as pd
import streamlit as st

from utils import (
    escape_markdown,
    highlight_html_fuzzy,
    normalize_text,
    retrieve_context_fuzzy,
)

st.caption("User Interface for all the records scrapped from the several EMR")
with open("data/full_tasy_records.json", "r") as f:
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
            records = json_data[rghc]

            if word_query:
                st.subheader("Search query results")
                for db, record in json_data[rghc].items():
                    clean_record = {
                        k: v
                        for k, v in record.items()
                        if not pd.isna(v) and not v == ""
                    }

                    full_text = normalize_text("\n".join(clean_record.values())).strip()
                    matches = retrieve_context_fuzzy(word_query, full_text, l_dist)
                    if matches:
                        st.markdown(f"{db} : {len(matches)} match(es) found")
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
                        st.info(db, "No match found")
            st.subheader("Full record(s)")
            for db, record in json_data[rghc].items():
                st.markdown(db)
                st.json(
                    {k: v for k, v in record.items() if v != "" and not pd.isna(v)},
                    expanded=False,
                )
    else:
        st.info("invalid rghc")
