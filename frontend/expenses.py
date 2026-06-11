import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def show_add_expense():
    st.title("Add Expense")

    categories = ["Food", "Transport", "Shopping", "Entertainment", "Bills", "Health", "Other"]

    with st.form("add_expense_form"):
        amount = st.number_input("Amount (₹)", min_value=0.01, step=0.01)
        category = st.selectbox("Category", categories)
        date = st.date_input("Date")
        description = st.text_input("Description (optional)")
        submitted = st.form_submit_button("Add Expense")

    if submitted:
        token = st.session_state.get("user_token")
        if not token:
            st.error("Not logged in.")
            return

        payload = {
            "amount": amount,
            "category": category,
            "date": str(date),
            "description": description if description else None
        }

        response = requests.post(
            f"{API_URL}/expenses/add",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code == 200:
            st.success("Expense added successfully!")
        else:
            st.error(f"Error: {response.json().get('detail', 'Something went wrong')}")