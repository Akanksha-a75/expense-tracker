import streamlit as st
from login import show_login

if "auth_stage" not in st.session_state or st.session_state.auth_stage != "verified":
    show_login()
    st.stop()

# ── Everything below only runs when logged in ──
st.write(f"Welcome, {st.session_state.user_email}!")