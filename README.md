# 💰 Expense Tracker

A full-stack Expense Tracker application built using **FastAPI**, **Streamlit**, and **MySQL** with **OTP-based email authentication**.

## 🚀 Features

### Authentication

* User Sign Up
* OTP-based Sign In
* Email OTP delivery using SMTP
* Secure OTP verification

### Expense Management

* Add Expense
* View Expenses
* Update Expenses
* Delete Expenses

### Database

* MySQL Integration
* User Management
* OTP Verification Records
* Expense Storage

---

## 🛠️ Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* MySQL
* SMTP (Gmail)

### Frontend

* Streamlit

### Database

* MySQL

### Version Control

* Git
* GitHub

---

## 📂 Project Structure

```text
expense_tracker/
│
├── backend/
│   ├── routes/
│   │   ├── auth.py
│   │   └── expenses.py
│   │
│   ├── utils/
│   │   ├── otp.py
│   │   └── email_sender.py
│   │
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/Akanksha-a75/expense-tracker.git
cd expense_tracker
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

#### macOS/Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Setup

Create a MySQL database:

```sql
CREATE DATABASE expense_tracker;
```

Configure database credentials in `.env`:

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=expense_tracker
```

---

## 📧 Email Configuration

Generate a Gmail App Password and configure:

```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

---

## ▶️ Run Backend

Navigate to backend folder:

```bash
cd backend
```

Start FastAPI server:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## ▶️ Run Frontend

Navigate to frontend folder:

```bash
cd frontend
```

Start Streamlit application:

```bash
streamlit run app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

## 📊 API Endpoints

### Authentication

| Method | Endpoint      | Description    |
| ------ | ------------- | -------------- |
| POST   | `/signup`     | Create Account |
| POST   | `/send-otp`   | Send OTP       |
| POST   | `/verify-otp` | Verify OTP     |

### Expenses

| Method | Endpoint         | Description      |
| ------ | ---------------- | ---------------- |
| GET    | `/expenses`      | Get All Expenses |
| POST   | `/expenses`      | Add Expense      |
| PUT    | `/expenses/{id}` | Update Expense   |
| DELETE | `/expenses/{id}` | Delete Expense   |

---

## 🎯 Future Improvements

* User-specific expense tracking
* Monthly analytics dashboard
* Expense category charts
* Download reports as CSV/PDF
* Budget tracking
* Expense filtering and search
* JWT Authentication

---

## 👩‍💻 Contributors

* Aditi Sharma
* Akanksha

---

## 📜 License

This project is created for educational and learning purposes.
