import sqlite3
import os
from datetime import datetime, timedelta
from typing import Optional, Tuple, List
from models.models import User, OTP, Expense

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "expense_tracker.db")


def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database with required tables"""
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create otps table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS otps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            otp_code TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            is_verified BOOLEAN DEFAULT 0,
            FOREIGN KEY (email) REFERENCES users(email)
        )
    """)

    # Create expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            expense_date TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def user_exists(email: str) -> bool:
    """Check if user exists in database"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()

    return result is not None


def create_user(name: str, email: str, phone: str) -> Tuple[bool, str]:
    """Create a new user in database"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name, email, phone) VALUES (?, ?, ?)",
            (name, email, phone)
        )

        conn.commit()
        conn.close()

        return True, "User created successfully"

    except sqlite3.IntegrityError:
        return False, "Email already exists"
    except Exception as e:
        return False, f"Error creating user: {str(e)}"


def get_user(email: str) -> Optional[User]:
    """Get user by email"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return User(
            id=result["id"],
            name=result["name"],
            email=result["email"],
            phone=result["phone"],
            created_at=datetime.fromisoformat(result["created_at"])
        )

    return None


def store_otp(email: str, otp_code: str, expiry_minutes: int = 5) -> Tuple[bool, str]:
    """Store OTP for user with expiration time"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Calculate expiration time
        expires_at = datetime.now() + timedelta(minutes=expiry_minutes)

        # Delete any existing unverified OTPs for this email
        cursor.execute(
            "DELETE FROM otps WHERE email = ? AND is_verified = 0",
            (email,)
        )

        # Insert new OTP
        cursor.execute(
            "INSERT INTO otps (email, otp_code, expires_at) VALUES (?, ?, ?)",
            (email, otp_code, expires_at.isoformat())
        )

        conn.commit()
        conn.close()

        return True, "OTP stored successfully"

    except Exception as e:
        return False, f"Error storing OTP: {str(e)}"


def verify_otp(email: str, otp_code: str) -> Tuple[bool, str]:
    """Verify OTP for user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Get the OTP
        cursor.execute(
            "SELECT * FROM otps WHERE email = ? AND is_verified = 0 ORDER BY created_at DESC LIMIT 1",
            (email,)
        )
        result = cursor.fetchone()

        if not result:
            conn.close()
            return False, "No OTP found. Please request a new OTP."

        # Check if OTP matches
        if result["otp_code"] != otp_code:
            conn.close()
            return False, "Invalid OTP"

        # Check if OTP has expired
        expires_at = datetime.fromisoformat(result["expires_at"])
        if datetime.now() > expires_at:
            conn.close()
            return False, "OTP has expired. Please request a new OTP."

        # Mark OTP as verified
        cursor.execute(
            "UPDATE otps SET is_verified = 1 WHERE id = ?",
            (result["id"],)
        )

        conn.commit()
        conn.close()

        return True, "OTP verified successfully"

    except Exception as e:
        return False, f"Error verifying OTP: {str(e)}"


def get_latest_otp(email: str) -> Optional[OTP]:
    """Get latest OTP for user"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM otps WHERE email = ? ORDER BY created_at DESC LIMIT 1",
        (email,)
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        return OTP(
            id=result["id"],
            email=result["email"],
            otp_code=result["otp_code"],
            created_at=datetime.fromisoformat(result["created_at"]),
            expires_at=datetime.fromisoformat(result["expires_at"]) if result["expires_at"] else None,
            is_verified=bool(result["is_verified"])
        )

    return None


# ==================== EXPENSE FUNCTIONS ====================

def add_expense(user_id: int, amount: float, category: str, expense_date: datetime, description: str = "") -> Tuple[bool, str, Optional[int]]:
    """Add a new expense for user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO expenses (user_id, amount, category, description, expense_date) VALUES (?, ?, ?, ?, ?)",
            (user_id, amount, category, description, expense_date.isoformat())
        )

        conn.commit()
        expense_id = cursor.lastrowid
        conn.close()

        return True, "Expense added successfully", expense_id

    except Exception as e:
        return False, f"Error adding expense: {str(e)}", None


def get_expense(expense_id: int) -> Optional[Expense]:
    """Get expense by ID"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return Expense(
            id=result["id"],
            user_id=result["user_id"],
            amount=result["amount"],
            category=result["category"],
            description=result["description"],
            expense_date=datetime.fromisoformat(result["expense_date"]),
            created_at=datetime.fromisoformat(result["created_at"])
        )

    return None


def get_user_expenses(user_id: int) -> List[Expense]:
    """Get all expenses for a user"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM expenses WHERE user_id = ? ORDER BY expense_date DESC",
        (user_id,)
    )
    results = cursor.fetchall()
    conn.close()

    expenses = []
    for result in results:
        expenses.append(Expense(
            id=result["id"],
            user_id=result["user_id"],
            amount=result["amount"],
            category=result["category"],
            description=result["description"],
            expense_date=datetime.fromisoformat(result["expense_date"]),
            created_at=datetime.fromisoformat(result["created_at"])
        ))

    return expenses


def get_user_expenses_by_month(user_id: int, year: int, month: int) -> List[Expense]:
    """Get expenses for a user in a specific month"""
    conn = get_connection()
    cursor = conn.cursor()

    # Get first and last day of month
    if month == 12:
        first_day = datetime(year, month, 1)
        last_day = datetime(year + 1, 1, 1)
    else:
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month + 1, 1)

    cursor.execute(
        "SELECT * FROM expenses WHERE user_id = ? AND expense_date >= ? AND expense_date < ? ORDER BY expense_date DESC",
        (user_id, first_day.isoformat(), last_day.isoformat())
    )
    results = cursor.fetchall()
    conn.close()

    expenses = []
    for result in results:
        expenses.append(Expense(
            id=result["id"],
            user_id=result["user_id"],
            amount=result["amount"],
            category=result["category"],
            description=result["description"],
            expense_date=datetime.fromisoformat(result["expense_date"]),
            created_at=datetime.fromisoformat(result["created_at"])
        ))

    return expenses


def delete_expense(expense_id: int) -> Tuple[bool, str]:
    """Delete an expense"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

        conn.commit()
        conn.close()

        return True, "Expense deleted successfully"

    except Exception as e:
        return False, f"Error deleting expense: {str(e)}"


def get_total_expenses(user_id: int) -> float:
    """Get total expenses for a user"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) as total FROM expenses WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()

    return result["total"] if result["total"] is not None else 0.0


def get_current_month_expenses(user_id: int) -> float:
    """Get total expenses for current month"""
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now()
    if now.month == 12:
        first_day = datetime(now.year, 12, 1)
        last_day = datetime(now.year + 1, 1, 1)
    else:
        first_day = datetime(now.year, now.month, 1)
        last_day = datetime(now.year, now.month + 1, 1)

    cursor.execute(
        "SELECT SUM(amount) as total FROM expenses WHERE user_id = ? AND expense_date >= ? AND expense_date < ?",
        (user_id, first_day.isoformat(), last_day.isoformat())
    )
    result = cursor.fetchone()
    conn.close()

    return result["total"] if result["total"] is not None else 0.0


def get_expense_count(user_id: int) -> int:
    """Get total number of expenses for a user"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as count FROM expenses WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()

    return result["count"]


def get_category_wise_summary(user_id: int) -> dict:
    """Get category-wise expense summary"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ? GROUP BY category",
        (user_id,)
    )
    results = cursor.fetchall()
    conn.close()

    summary = {}
    for result in results:
        summary[result["category"]] = result["total"]

    return summary


def get_monthly_summary(user_id: int, months: int = 12) -> dict:
    """Get monthly expense summary for last N months"""
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now()
    summary = {}

    for i in range(months):
        month_date = now.replace(day=1) - timedelta(days=i * 30)
        month_date = month_date.replace(day=1)
        year = month_date.year
        month = month_date.month

        if month == 12:
            first_day = datetime(year, month, 1)
            last_day = datetime(year + 1, 1, 1)
        else:
            first_day = datetime(year, month, 1)
            last_day = datetime(year, month + 1, 1)

        cursor.execute(
            "SELECT SUM(amount) as total FROM expenses WHERE user_id = ? AND expense_date >= ? AND expense_date < ?",
            (user_id, first_day.isoformat(), last_day.isoformat())
        )
        result = cursor.fetchone()
        month_key = month_date.strftime("%B %Y")
        summary[month_key] = result["total"] if result["total"] is not None else 0.0

    conn.close()
    return summary
