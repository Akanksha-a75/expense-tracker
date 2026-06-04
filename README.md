# Expense Tracker

A multi-user expense tracking web application built with **FastAPI**, **Streamlit**, and **PostgreSQL** — featuring OTP-based authentication, budget alerts, recurring expenses, and analytics dashboards.

---

## Features

- **Expense Management** — Add, edit, delete, and categorise your expenses
- **Budget Limits & Alerts** — Set monthly budgets per category and get notified when you cross them
- **Recurring Expenses** — Track fixed bills, rent, and subscriptions automatically
- **Analytics Dashboard** — Visualise spending trends, category breakdowns, and monthly/weekly summaries
- **Multi-User Support** — Each user has a separate account and sees only their own data
- **OTP Authentication** — Secure login via a 6-digit one-time password sent to your Gmail

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Database | PostgreSQL |
| Authentication | OTP via Gmail SMTP |
| Dependency Management | Poetry |

---

## Architecture

```
User
  ↓
Streamlit UI  (login, register, dashboard, charts)
  ↓
FastAPI Backend  (API routes, request handling)
  ↓
Auth Module ──────────────→ Gmail SMTP (sends OTP to user email)
  ↓
Business Logic  (validations, budget alert rules)
  ↓
┌─────────────┬──────────────┬──────────────┬─────────────────┐
│ Expense     │ Budget       │ Recurring    │ Analytics       │
│ Module      │ Module       │ Module       │ Module          │
│ add/edit/   │ limits,      │ bills, subs, │ charts, trends, │
│ delete      │ alerts       │ rent         │ summaries       │
└─────────────┴──────────────┴──────────────┴─────────────────┘
  ↓
Data Access Layer  (SQL queries, CRUD operations)
  ↓
PostgreSQL Database  (users, expenses, budgets, OTPs)
```

---

## Project Structure

```
expense-tracker/
├── backend/
│   └── app/
│       ├── main.py              # FastAPI entry point
│       ├── database.py          # PostgreSQL connection
│       ├── models.py            # Database table definitions
│       ├── schemas.py           # Request/response shapes
│       ├── auth/
│       │   ├── otp.py           # OTP generate & verify
│       │   ├── smtp.py          # Gmail SMTP email sender
│       │   └── session.py       # Session management
│       └── routes/
│           ├── expenses.py      # Expense CRUD routes
│           ├── budgets.py       # Budget limit routes
│           ├── recurring.py     # Recurring expense routes
│           └── analytics.py     # Charts & summary routes
├── frontend/
│   └── app.py                   # Streamlit UI
├── .env                         # Secrets (not pushed to GitHub)
├── .gitignore
├── README.md
└── pyproject.toml               # Poetry dependencies
```

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- PostgreSQL installed and running
- A Gmail account with App Password enabled
- Poetry installed

### 1. Clone the repository
```bash
git clone https://github.com/Akanksha-a75/expense-tracker.git
cd expense-tracker
```

### 2. Install dependencies
```bash
poetry install
```

### 3. Set up environment variables

Create a `.env` file in the root directory:
```
DATABASE_URL=postgresql://username:password@localhost/expense_tracker
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
SECRET_KEY=your-secret-key
```

### 4. Run the backend
```bash
poetry run uvicorn backend.app.main:app --reload
```

### 5. Run the frontend
```bash
poetry run streamlit run frontend/app.py
```

---

## Team

| Name | GitHub |
|---|---|
| Akanksha | [@Akanksha-a75](https://github.com/Akanksha-a75) |
| Aditi | [@anna8668](https://github.com/anna8668) |
