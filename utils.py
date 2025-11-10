import re
import unicodedata
from io import StringIO
from typing import List

import pandas as pd
import streamlit as st
from fuzzysearch import find_near_matches


def text_search(
    regex_pattern: str,
    df: pd.DataFrame,
    text_column: str,
) -> pd.DataFrame:
    return df[df[text_column].str.contains(pat=regex_pattern, regex=True)]


def text_search_fuzzy(
    word_query: str,
    df: pd.DataFrame,
    text_column: str,
    max_l_dist: int,
) -> pd.DataFrame:
    return df[
        df[text_column].apply(
            lambda t: bool(
                find_near_matches(
                    word_query, t, max_l_dist, max_l_dist, max_l_dist, max_l_dist
                )
            )
        )
    ]


# ---------- Helpers ----------
@st.cache_data(show_spinner=False)
def load_csv(file_bytes: bytes) -> pd.DataFrame:
    """Robust CSV loader that tries UTF-8 then Latin-1.
    Returns a DataFrame with all columns as-is.
    """
    try:
        return pd.read_csv(StringIO(file_bytes.decode("utf-8")))
    except UnicodeDecodeError:
        return pd.read_csv(StringIO(file_bytes.decode("latin-1")))


def escape_markdown(text: str) -> str:
    # Escape common Markdown characters
    return re.sub(r"([*_#`>\[\]\(\)\-])", r"\\\1", text)


def normalize_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


# ---------- Result visualization ----------
def retrieve_context(query: str, text: str) -> List:
    match_context = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.search(query, line):
            prev_line = lines[i - 1] if i > 0 else ""
            curr_line = line
            next_line = lines[i + 1] if i < len(lines) - 1 else ""
            match_context.append(prev_line + "\n" + curr_line + "\n" + next_line)
    return match_context


def retrieve_context_fuzzy(query: str, text: str, max_l_dist: int = 1) -> List:
    match_context = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        # if re.search(query, line):
        if find_near_matches(query, line, max_l_dist=max_l_dist):
            prev_line = lines[i - 1] if i > 0 else ""
            curr_line = line
            next_line = lines[i + 1] if i < len(lines) - 1 else ""
            match_context.append(prev_line + "\n" + curr_line + "\n" + next_line)
    return match_context


def highlight_html(s: str, text: str) -> str:
    """Return HTML with <mark> tags around matches."""
    pattern = re.compile(re.escape(s))
    highlighted = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)
    return highlighted


def highlight_html_fuzzy(query: str, text: str, max_l_dist: int = 1) -> str:
    """Return HTML with <mark> tags around fuzzy matches of `query` in `text`."""
    matches = find_near_matches(query, text, max_l_dist=max_l_dist)
    if not matches:
        return text

    # Sort descending so inserts don’t shift later indices
    matches = sorted(matches, key=lambda m: m.start, reverse=True)

    for m in matches:
        text = text[: m.end] + "</mark>" + text[m.end :]
        text = text[: m.start] + "<mark>" + text[m.start :]

    return text


# ---------- Data wrapper ----------
@st.cache_data
def convert_for_download(df):
    return df.to_csv().encode("utf-8")
