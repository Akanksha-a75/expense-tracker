import streamlit as st
import requests
from datetime import datetime

API_BASE = "http://127.0.0.1:8000"
CATEGORIES = ["Food", "Transport", "Shopping", "Entertainment", "Health", "Other"]

def show_view_expenses():
    st.title("My Expenses")

    token = st.session_state.get("user_token")
    if not token:
        st.error("Not logged in.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE}/expenses/list", headers=headers)

    if response.status_code != 200:
        st.error("Failed to load expenses.")
        return

    expenses = response.json()
    if not expenses:
        st.info("No expenses added yet.")
        return

    for expense in expenses:
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 2, 2, 2, 3, 1, 1])
        col1.write(expense["id"])
        col2.write(f"₹{expense['amount']}")
        col3.write(expense["category"])
        col4.write(expense["date"])
        col5.write(expense["description"] or "—")

        if col6.button("✏️", key=f"edit_{expense['id']}"):
            st.session_state[f"editing_{expense['id']}"] = True

        if col7.button("🗑️", key=f"del_{expense['id']}"):
            del_res = requests.delete(f"{API_BASE}/expenses/{expense['id']}", headers=headers)
            if del_res.status_code == 200:
                st.success("Deleted!")
                st.rerun()
            else:
                st.error("Failed to delete.")

        if st.session_state.get(f"editing_{expense['id']}"):
            with st.form(key=f"form_{expense['id']}"):
                new_amount = st.number_input("Amount", value=float(expense["amount"]), min_value=0.01, step=0.01)
                new_category = st.selectbox("Category", CATEGORIES, index=CATEGORIES.index(expense["category"]))
                new_date = st.date_input("Date", value=datetime.strptime(expense["date"], "%Y-%m-%d").date())
                new_description = st.text_input("Description", value=expense["description"] or "")
                submitted = st.form_submit_button("Save Changes")
                cancelled = st.form_submit_button("Cancel")

                if submitted:
                    payload = {
                        "amount": new_amount,
                        "category": new_category,
                        "date": str(new_date),
                        "description": new_description if new_description else None
                    }
                    res = requests.put(f"{API_BASE}/expenses/{expense['id']}", json=payload, headers=headers)
                    if res.status_code == 200:
                        st.success("Updated!")
                        st.session_state[f"editing_{expense['id']}"] = False
                        st.rerun()
                    else:
                        st.error("Failed to update.")

                if cancelled:
                    st.session_state[f"editing_{expense['id']}"] = False
                    st.rerun()