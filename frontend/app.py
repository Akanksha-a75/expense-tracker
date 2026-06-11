import streamlit as st
from login import show_login
from expenses import show_add_expense
from view_expenses import show_view_expenses

if "auth_stage" not in st.session_state or st.session_state.auth_stage != "verified":
    show_login()
    st.stop()

# — Everything below only runs when logged in —
st.sidebar.title("Menu")
page = st.sidebar.radio("Navigate", ["Home", "Add Expense", "View Expenses"])

if page == "Home":
    st.write(f"Welcome, {st.session_state.user_email}!")

elif page == "Add Expense":
    show_add_expense()

elif page == "View Expenses":
    show_view_expenses()