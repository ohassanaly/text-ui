import registro.redcap as red
import streamlit as st

# ---------------- Token state setup ----------------
if "token" not in st.session_state:
    st.session_state.token = None

st.caption("Consult Redcap API")

token = st.text_input(
    "Redcap token",
    placeholder="Enter your Redcap authentication token",
    type="password",
)

if token:
    st.session_state.token = token

    with st.form("Redcap API"):
        input_rghc = st.text_input("rghc", placeholder="Enter a rghc")

        input_var = st.text_input(
            "Variables", placeholder="Enter the variables you are interested in"
        )

        input_filter = st.text_input("Filter", placeholder="(optional) enter a filter")

        submit_search = st.form_submit_button("API Search")

    if submit_search:
        try:
            df = red.extrair(token, input_var, filtro=input_filter, rghc_ls=input_rghc)
            st.dataframe(df)
        except Exception as e:
            st.warning("Invalid input data", e)
