import time

import streamlit as st
from registro import exames

# ---------------- Login state setup ----------------
if "authed" not in st.session_state:
    st.session_state.authed = False
if "s_hc" not in st.session_state:
    st.session_state.s_hc = None

st.caption("Retrieve lab exams based on HCMed records")

# ---------------- Login ----------------
with st.form("HCMed Login"):
    username = st.text_input("username", placeholder="Enter your HCMed username")
    password = st.text_input(
        "password", placeholder="Enter your HCMed password", type="password"
    )
    submit_login = st.form_submit_button("Login")

# ---------------- Lab exams extraction ----------------
if submit_login:
    try:
        s_hc = exames.hc_login()
        s_hc.logar(username, password)
        st.session_state.s_hc = s_hc
        st.session_state.authed = True
        st.success("Logged in.")
    except Exception as e:
        st.session_state.authed = False
        st.session_state.s_hc = None
        st.error(f"Login failed: {e}")

if st.session_state.authed:
    with st.form("Exam details"):
        input_rhgc = st.text_input(
            "rghc", placeholder="Enter a rghc to access its lab exams"
        )

        exam_type = st.text_input(
            "Exam type", placeholder="Enter the type of exam you wish"
        )

        return_mode = st.radio(
            label="Return type",
            options=["all", "first", "last", "target"],
            captions=[
                "todos os resultados",
                "o primeiro resultado",
                "o ultimo resultado",
                "o exame mais proximo da data ini_dt",
            ],
            horizontal=True,
        )

        initial_date = st.text_input("Initial date", placeholder="format dd/mm/yyyy")

        submit_exam = st.form_submit_button("Extract lab results")

    if submit_exam:
        with st.spinner("Connecting to HCMed (wait at least 5-10 seconds)"):
            time.sleep(10)

        s_hc = exames.hc_login()
        s_hc.logar(username, password)

        result = exames.res_lab(
            exames.links(s_hc, rghc=input_rhgc),
            exam_type,
            extrair=return_mode,
            ini_dt=initial_date,
        )
        st.dataframe(result)
    else:
        st.info("Register both rghc, exam type, return type and initial date")
