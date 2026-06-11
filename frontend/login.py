import streamlit as st
import requests

API_BASE = "http://localhost:8000"

def show_login():
    st.title("💸 Group Expense Tracker")

    if "auth_stage" not in st.session_state:
        st.session_state.auth_stage = "entry"  # stages: entry → otp_sent → verified

    if "auth_email" not in st.session_state:
        st.session_state.auth_email = ""

    # ── Stage 1: Email entry ──────────────────────────────────────────
    if st.session_state.auth_stage == "entry":
        st.subheader("Sign in / Sign up")
        st.caption("We'll send a one-time password to your email.")

        email = st.text_input("Email address", placeholder="you@example.com")

        if st.button("Send OTP", use_container_width=True):
            if not email or "@" not in email:
                st.error("Please enter a valid email.")
            else:
                with st.spinner("Sending OTP..."):
                    try:
                        res = requests.post(f"{API_BASE}/auth/send-otp", json={"email": email})
                        if res.status_code == 200:
                            st.session_state.auth_email = email
                            st.session_state.auth_stage = "otp_sent"
                            st.rerun()
                        else:
                            st.error(res.json().get("detail", "Something went wrong."))
                    except Exception:
                        st.error("Cannot reach server. Is the backend running?")

    # ── Stage 2: OTP verification ─────────────────────────────────────
    elif st.session_state.auth_stage == "otp_sent":
        st.subheader("Enter OTP")
        st.caption(f"OTP sent to **{st.session_state.auth_email}**")

        otp = st.text_input("6-digit OTP", max_chars=6, placeholder="123456")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Verify OTP", use_container_width=True):
                if len(otp) != 6 or not otp.isdigit():
                    st.error("Enter a valid 6-digit OTP.")
                else:
                    with st.spinner("Verifying..."):
                        try:
                            res = requests.post(f"{API_BASE}/auth/verify-otp", json={
                                "email": st.session_state.auth_email,
                                "otp": otp
                            })
                            if res.status_code == 200:
                                data = res.json()
                                st.session_state.auth_stage = "verified"
                                st.session_state.user_token = data.get("token")
                                st.session_state.user_email = st.session_state.auth_email
                                st.rerun()
                            else:
                                st.error(res.json().get("detail", "Invalid or expired OTP."))
                        except Exception:
                            st.error("Cannot reach server. Is the backend running?")

        with col2:
            if st.button("← Back", use_container_width=True):
                st.session_state.auth_stage = "entry"
                st.rerun()