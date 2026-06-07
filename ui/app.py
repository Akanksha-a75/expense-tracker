import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.auth_service import send_otp, verify_otp, register_user
from services.expense_service import (
    create_expense,
    get_user_expense_history,
    remove_expense,
    get_dashboard_metrics,
    get_recent_expenses,
    get_category_summary,
    get_monthly_expense_summary
)
from database.db import init_db, get_user

# Initialize database
init_db()

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# ---------------- SESSION STATE ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False

# ---------------- LOGIN PAGE ----------------

if not st.session_state.logged_in:

    st.title("💰 AI Expense Tracker")

    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])

    # ---------------- SIGN UP ----------------

    with tab2:

        st.subheader("Create Account")

        name = st.text_input(
            "Full Name",
            key="signup_name"
        )

        phone = st.text_input(
            "Phone Number",
            key="signup_phone"
        )

        email_signup = st.text_input(
            "Email Address",
            key="signup_email"
        )

        if st.button("Create Account", key="signup_btn"):

            if not name or not phone or not email_signup:
                st.warning("Please fill in all fields")

            else:
                success, message = register_user(name, email_signup, phone)

                if success:
                    st.success("Account Created Successfully! Please sign in.")

                else:
                    st.error(message)

    # ---------------- SIGN IN ----------------

    with tab1:

        st.subheader("Sign In")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        if st.button("Send OTP", key="send_otp_btn"):

            if email == "":
                st.warning("Please enter email")

            else:
                success, message, otp = send_otp(email)

                if success:
                    st.session_state.user_email = email
                    st.session_state.otp_sent = True
                    st.success(message)
                    st.rerun()

                else:
                    st.error(message)

        # Show OTP input only if OTP was sent
        if st.session_state.otp_sent:

            st.divider()

            otp_input = st.text_input(
                "Enter OTP",
                key="login_otp"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Verify OTP", key="verify_otp_btn"):

                    if not otp_input:
                        st.warning("Please enter OTP")

                    else:
                        success, message = verify_otp(
                            st.session_state.user_email,
                            otp_input
                        )

                        if success:
                            # Get user ID for database operations
                            user = get_user(st.session_state.user_email)
                            if user:
                                st.session_state.logged_in = True
                                st.session_state.user_email = st.session_state.user_email
                                st.session_state.user_id = user.id
                                st.success("Login Successful!")
                                st.rerun()
                            else:
                                st.error("User not found")

                        else:
                            st.error(message)

            with col2:
                if st.button("Request New OTP", key="new_otp_btn"):
                    st.session_state.otp_sent = False
                    st.rerun()

# ---------------- DASHBOARD ----------------

else:

    st.sidebar.title("Expense Tracker")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Add Expense",
            "Expense History",
            "Reports",
            "Profile"
        ]
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.user_id = None
        st.session_state.otp_sent = False

        st.rerun()

    # ---------------- DASHBOARD ----------------

    if page == "Dashboard":

        st.title("Dashboard")

        # Get dashboard metrics from database
        success, message, metrics = get_dashboard_metrics(st.session_state.user_id)

        if success:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Total Expense",
                    f"₹{metrics['total_expenses']:,.2f}"
                )

            with col2:
                st.metric(
                    "This Month",
                    f"₹{metrics['current_month_expenses']:,.2f}"
                )

            with col3:
                st.metric(
                    "Transactions",
                    metrics['transaction_count']
                )
        else:
            st.error(message)

        st.divider()

        st.subheader("Recent Expenses")

        # Get recent expenses from database
        success, message, recent_expenses = get_recent_expenses(st.session_state.user_id, limit=10)

        if success and recent_expenses:
            st.dataframe(
                {
                    "Date": [expense["date"] for expense in recent_expenses],
                    "Category": [expense["category"] for expense in recent_expenses],
                    "Amount": [f"₹{expense['amount']:.2f}" for expense in recent_expenses],
                    "Description": [expense["description"] for expense in recent_expenses]
                },
                use_container_width=True
            )
        elif success and not recent_expenses:
            st.info("No expenses yet. Add your first expense!")
        else:
            st.error(message)

    # ---------------- ADD EXPENSE ----------------

    elif page == "Add Expense":

        st.title("Add Expense")

        with st.form("add_expense_form"):
            amount = st.number_input(
                "Amount (₹)",
                min_value=0.0,
                step=0.01
            )

            category = st.selectbox(
                "Category",
                [
                    "Food",
                    "Travel",
                    "Shopping",
                    "Bills",
                    "Health",
                    "Entertainment",
                    "Education",
                    "Other"
                ]
            )

            expense_date = st.date_input(
                "Expense Date",
                value=datetime.now().date()
            )

            description = st.text_area(
                "Description (Optional)",
                height=100
            )

            submitted = st.form_submit_button("Add Expense")

            if submitted:
                if amount <= 0:
                    st.error("Please enter a valid amount greater than 0")
                else:
                    # Convert date to datetime
                    expense_datetime = datetime.combine(expense_date, datetime.min.time())
                    
                    success, message = create_expense(
                        st.session_state.user_id,
                        amount,
                        category,
                        expense_datetime,
                        description
                    )

                    if success:
                        st.success("Expense Added Successfully!")
                        # Clear form by rerunning
                        st.rerun()
                    else:
                        st.error(message)

    # ---------------- HISTORY ----------------

    elif page == "Expense History":

        st.title("Expense History")

        # Get user's expense history
        success, message, expenses = get_user_expense_history(st.session_state.user_id)

        if success and expenses:
            # Create dataframe for display
            df_data = {
                "ID": [expense["id"] for expense in expenses],
                "Date": [expense["date"] for expense in expenses],
                "Category": [expense["category"] for expense in expenses],
                "Amount": [f"₹{expense['amount']:.2f}" for expense in expenses],
                "Description": [expense["description"] for expense in expenses]
            }

            col1, col2 = st.columns([4, 1])

            with col1:
                st.dataframe(df_data, use_container_width=True)

            # Add delete functionality
            st.divider()
            st.subheader("Delete Expense")

            expense_ids = [str(exp["id"]) for exp in expenses]
            expense_display = [f"{exp['date']} - {exp['category']} - ₹{exp['amount']}" for exp in expenses]

            selected_expense = st.selectbox(
                "Select expense to delete:",
                expense_ids,
                format_func=lambda x: expense_display[expense_ids.index(x)]
            )

            if st.button("Delete Selected Expense"):
                expense_id = int(selected_expense)
                success, message = remove_expense(expense_id, st.session_state.user_id)

                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        elif success and not expenses:
            st.info("No expenses found. Add your first expense!")
        else:
            st.error(message)

    # ---------------- REPORTS ----------------

    elif page == "Reports":

        st.title("Reports & Analytics")

        # Category-wise summary
        st.subheader("Category-wise Summary")

        success, message, category_summary = get_category_summary(st.session_state.user_id)

        if success and category_summary and category_summary.get("Category"):
            st.bar_chart(
                {
                    "Category": category_summary["Category"],
                    "Amount": category_summary["Amount"]
                },
                x="Category",
                y="Amount"
            )
        elif success and not category_summary.get("Category"):
            st.info("No expense data available for category summary")
        else:
            st.error(message)

        st.divider()

        # Monthly summary
        st.subheader("Monthly Expense Trend")

        success, message, monthly_summary = get_monthly_expense_summary(st.session_state.user_id, months=6)

        if success and monthly_summary and monthly_summary.get("Month"):
            st.line_chart(
                {
                    "Month": monthly_summary["Month"],
                    "Amount": monthly_summary["Amount"]
                },
                x="Month",
                y="Amount"
            )
        elif success and not monthly_summary.get("Month"):
            st.info("No expense data available for monthly summary")
        else:
            st.error(message)

    # ---------------- PROFILE ----------------

    elif page == "Profile":

        st.title("Profile")

        user = get_user(st.session_state.user_email)

        if user:
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Name:** {user.name}")
                st.write(f"**Email:** {user.email}")

            with col2:
                st.write(f"**Phone:** {user.phone}")
                st.write(f"**Member Since:** {user.created_at.strftime('%d-%m-%Y')}")
        else:
            st.error("User information not found")