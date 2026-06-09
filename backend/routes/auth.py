from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import (
    SendOTPRequest,
    VerifyOTPRequest,
    CreateUserRequest
)
from database import get_db
from models import OTPVerification, User
from utils.email_sender import send_otp_email
import random

router = APIRouter()

@router.post("/send-otp")
def send_otp(data: SendOTPRequest, db: Session = Depends(get_db)):

    otp = str(random.randint(100000, 999999))

    otp_entry = OTPVerification(
        email=data.email,
        otp=otp,
        is_verified="False"
    )

    db.add(otp_entry)
    db.commit()

    send_otp_email(data.email, otp)

    return {
        "email": data.email,
        "message": "OTP Sent Successfully"
    }

@router.post("/signup")
def signup(
    data: CreateUserRequest,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:
        return {
            "message": "Account already exists"
        }

    new_user = User(
        name=data.name,
        email=data.email
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "Account Created Successfully"
    }

@router.post("/verify-otp")
def verify_otp(data: VerifyOTPRequest, db: Session = Depends(get_db)):

    otp_record = db.query(OTPVerification).filter(
        OTPVerification.email == data.email,
        OTPVerification.otp == data.otp
    ).first()

    if not otp_record:
        return {"message": "Invalid OTP"}

    otp_record.is_verified = "True"
    db.commit()

    return {
        "message": "OTP Verified Successfully"
    }