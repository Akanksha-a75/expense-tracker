import streamlit as st
import requests

st.set_page_config(
page_title="Expense Tracker",
page_icon="💰",
layout="centered"
)

# =========================

# SESSION STATE

# =========================

# =========================
# SESSION STATE
# =========================

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# =========================
# DASHBOARD
# =========================
# =========================
# DASHBOARD
# =========================

if st.session_state["logged_in"]:

    st.title("📊 Expense Dashboard")
    st.success("Welcome to Expense Tracker")

    # =========================
    # ADD EXPENSE
    # =========================

    st.subheader("➕ Add Expense")

    amount = st.number_input(
        "Amount",
        min_value=1
    )

    category = st.text_input(
        "Category"
    )

    description = st.text_input(
        "Description"
    )

    if st.button("Add Expense"):

        response = requests.post(
            "http://127.0.0.1:8000/expenses",
            json={
                "user_id": 1,
                "amount": amount,
                "category": category,
                "description": description
            }
        )

        st.success(response.json()["message"])

    # =========================
    # VIEW EXPENSES
    # =========================

    st.subheader("📋 View Expenses")

    try:

        response = requests.get(
            "http://127.0.0.1:8000/expenses"
        )

        expenses = response.json()

        if expenses:
            st.dataframe(
                expenses,
                use_container_width=True
            )
        else:
            st.info("No expenses found.")

    except Exception as e:

        st.error(
            f"Error loading expenses: {e}"
        )

    # =========================
    # UPDATE EXPENSE
    # =========================

    st.subheader("✏️ Update Expense")

    expense_id = st.number_input(
        "Expense ID",
        min_value=1,
        key="update_id"
    )

    new_amount = st.number_input(
        "New Amount",
        min_value=1,
        key="update_amount"
    )

    new_category = st.text_input(
        "New Category",
        key="update_category"
    )

    new_description = st.text_input(
        "New Description",
        key="update_description"
    )

    if st.button("Update Expense"):

        response = requests.put(
            f"http://127.0.0.1:8000/expenses/{expense_id}",
            json={
                "user_id": 1,
                "amount": new_amount,
                "category": new_category,
                "description": new_description
            }
        )

        st.success(
            response.json()["message"]
        )

    # =========================
    # DELETE EXPENSE
    # =========================

    st.subheader("🗑️ Delete Expense")

    delete_id = st.number_input(
        "Expense ID To Delete",
        min_value=1,
        key="delete_id"
    )

    if st.button("Delete Expense"):

        response = requests.delete(
            f"http://127.0.0.1:8000/expenses/{delete_id}"
        )

        st.success(
            response.json()["message"]
        )

    st.divider()

    if st.button("Logout"):

        st.session_state["logged_in"] = False
        st.rerun()

    st.stop()


# =========================

# AUTH PAGE

# =========================

st.title("💰 Expense Tracker")

tab1, tab2 = st.tabs(
["Sign In", "Sign Up"]
)

# =========================

# SIGN IN

# =========================

with tab1:

    st.subheader("Sign In")

    signin_email = st.text_input(
        "Email Address",
        key="signin_email"
    )

    if st.button(
        "Send OTP",
        key="signin_send_otp"
    ):

        response = requests.post(
            "http://127.0.0.1:8000/send-otp",
            json={
                "email": signin_email
            }
        )

        result = response.json()

        st.success(
            result["message"]
        )

    signin_otp = st.text_input(
        "Enter OTP",
        key="signin_otp"
    )

    if st.button(
        "Verify OTP",
        key="signin_verify_otp"
    ):

        response = requests.post(
            "http://127.0.0.1:8000/verify-otp",
            json={
                "email": signin_email,
                "otp": signin_otp
            }
        )

        result = response.json()

        if result["message"] == "OTP Verified Successfully":

            st.session_state["logged_in"] = True
            st.rerun()

        else:

            st.error(
                result["message"]
            )

# =========================

# SIGN UP

# =========================

with tab2:

    st.subheader("Create Account")

    signup_name = st.text_input(
        "Full Name",
        key="signup_name"
    )

    signup_email = st.text_input(
        "Email Address",
        key="signup_email"
    )

    if st.button(
        "Create Account",
        key="signup_create_account"
    ):

        response = requests.post(
            "http://127.0.0.1:8000/signup",
            json={
                "name": signup_name,
                "email": signup_email
            }
        )

        result = response.json()

        st.success(
            result["message"]
        )
