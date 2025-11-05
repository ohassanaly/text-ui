from io import StringIO
import pandas as pd
import streamlit as st
import re
# from termcolor import colored
from typing import List

# def exact_text_search(df: pd.DataFrame, text_column: str, s:str) -> pd.DataFrame:
#     #logical  (improve to manage priorities)
#     q = re.sub(r'\s(AND|OR)\s', lambda m: '|' if m.group(1) == 'OR' else ' ', s)
#     return(df[df["full_text"].str.contains(pat= q, regex =True)])
def text_search(regex_pattern:str, df:pd.DataFrame, text_column: str,) -> pd.DataFrame:
    return(df[df[text_column].str.contains(pat= regex_pattern, regex =True)])

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
    return re.sub(r'([*_#`>\[\]\(\)\-])', r'\\\1', text)

# ---------- Result visualization ----------
def retrieve_context(query:str, text:str) -> List:
    match_context = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.search(query, line):
            prev_line = lines[i-1] if i > 0 else ""
            curr_line = line
            next_line = lines[i+1] if i < len(lines) - 1 else ""
            match_context.append(prev_line+"\n"+curr_line+"\n"+next_line)
    return(match_context)

def highlight_html(s: str, text: str) -> str:
    """Return HTML with <mark> tags around matches."""
    pattern = re.compile(re.escape(s))
    highlighted = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)
    return highlighted