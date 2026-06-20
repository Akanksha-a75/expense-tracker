import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

def show_login():
    st.title("💰 Expense Tracker")

    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])

    # ── SIGN IN TAB ──────────────────────────────────────
    with tab1:
        st.subheader("Sign In")

        if "signin_stage" not in st.session_state:
            st.session_state.signin_stage = "entry"

        if st.session_state.signin_stage == "entry":
            email = st.text_input("Email Address", key="signin_email")
            if st.button("Send OTP", key="signin_send"):
                if not email:
                    st.error("Please enter your email.")
                else:
                    try:
                        res = requests.post(f"{API_BASE}/auth/send-otp", json={"email": email})
                        if res.status_code == 200:
                            st.session_state.signin_email_val = email
                            st.session_state.signin_stage = "otp_sent"
                            st.rerun()
                        else:
                            st.error(res.json().get("detail", "Something went wrong."))
                    except:
                        st.error("Cannot reach server. Is the backend running?")

        elif st.session_state.signin_stage == "otp_sent":
            st.info(f"OTP sent to **{st.session_state.signin_email_val}**")
            otp = st.text_input("Enter OTP", key="signin_otp")
            if st.button("Verify OTP", key="signin_verify"):
                try:
                    res = requests.post(f"{API_BASE}/auth/verify-otp", json={
                        "email": st.session_state.signin_email_val,
                        "otp": otp
                    })
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.auth_stage = "verified"
                        st.session_state.user_token = data.get("token")
                        st.session_state.user_email = st.session_state.signin_email_val
                        st.rerun()
                    else:
                        st.error(res.json().get("detail", "Invalid or expired OTP."))
                except:
                    st.error("Cannot reach server. Is the backend running?")

            if st.button("← Back", key="signin_back"):
                st.session_state.signin_stage = "entry"
                st.rerun()

    # ── SIGN UP TAB ──────────────────────────────────────
    with tab2:
        st.subheader("Create Account")

        if "signup_stage" not in st.session_state:
            st.session_state.signup_stage = "entry"

        if st.session_state.signup_stage == "entry":
            name = st.text_input("Full Name", key="signup_name")
            email = st.text_input("Email Address", key="signup_email")
            if st.button("Create Account", key="signup_btn"):
                if not name or not email:
                    st.error("Please fill in all fields.")
                else:
                    try:
                        res = requests.post(f"{API_BASE}/auth/signup", json={
                            "name": name,
                            "email": email
                        })
                        if res.status_code == 200:
                            st.session_state.signup_email_val = email
                            st.session_state.signup_stage = "otp_sent"
                            st.rerun()
                        else:
                            st.error(res.json().get("detail", "Something went wrong."))
                    except:
                        st.error("Cannot reach server. Is the backend running?")

        elif st.session_state.signup_stage == "otp_sent":
            st.info(f"OTP sent to **{st.session_state.signup_email_val}**")
            otp = st.text_input("Enter OTP", key="signup_otp")
            if st.button("Verify OTP", key="signup_verify"):
                try:
                    res = requests.post(f"{API_BASE}/auth/verify-otp", json={
                        "email": st.session_state.signup_email_val,
                        "otp": otp
                    })
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.auth_stage = "verified"
                        st.session_state.user_token = data.get("token")
                        st.session_state.user_email = st.session_state.signup_email_val
                        st.rerun()
                    else:
                        st.error(res.json().get("detail", "Invalid or expired OTP."))
                except:
                    st.error("Cannot reach server. Is the backend running?")

            if st.button("← Back", key="signup_back"):
                st.session_state.signup_stage = "entry"
                st.rerun()