import random
import smtplib
import sys
import os
from email.mime.text import MIMEText
from typing import Tuple

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.db import (
    user_exists,
    create_user,
    store_otp,
    verify_otp as db_verify_otp
)

# Gmail credentials
EMAIL = "aditi404sharma@gmail.com"
APP_PASSWORD = "hbcz jcfu xfpv jtli"


def generate_otp() -> str:
    """Generate a random 6-digit OTP"""
    return str(random.randint(100000, 999999))


def send_otp(email: str) -> Tuple[bool, str, str]:
    """
    Send OTP to user email and store in database.
    
    Args:
        email: User email address
        
    Returns:
        Tuple of (success: bool, message: str, otp_code: str)
    """
    try:
        # Check if user exists
        if not user_exists(email):
            return False, "Account not found. Please sign up first.", ""

        # Generate OTP
        otp = generate_otp()

        # Store OTP in database
        success, db_message = store_otp(email, otp)
        if not success:
            return False, db_message, ""

        # Send OTP via email
        msg = MIMEText(
            f"""
Your Expense Tracker OTP is:

{otp}

This OTP will expire in 5 minutes.
Do not share this OTP with anyone.
"""
        )

        msg["Subject"] = "Expense Tracker OTP"
        msg["From"] = EMAIL
        msg["To"] = email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, APP_PASSWORD)
            server.send_message(msg)

        return True, "OTP sent successfully", otp

    except Exception as e:
        return False, f"Failed to send OTP: {str(e)}", ""


def verify_otp(email: str, user_otp: str) -> Tuple[bool, str]:
    """
    Verify OTP for user.
    
    Args:
        email: User email address
        user_otp: OTP entered by user
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    return db_verify_otp(email, user_otp)


def register_user(name: str, email: str, phone: str) -> Tuple[bool, str]:
    """
    Register a new user.
    
    Args:
        name: User's full name
        email: User's email address
        phone: User's phone number
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    # Validate inputs
    if not name or not email or not phone:
        return False, "Please fill in all fields"

    # Check if user already exists
    if user_exists(email):
        return False, "Email already registered. Please sign in instead."

    # Create user in database
    return create_user(name, email, phone)