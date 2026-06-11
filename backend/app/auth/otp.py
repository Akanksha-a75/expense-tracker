import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import OTPCode

def generate_otp():
    return str(random.randint(100000, 999999))

def save_otp(db: Session, email: str, otp: str):
    # delete any existing OTP for this email
    db.query(OTPCode).filter(OTPCode.email == email).delete()
    
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    otp_entry = OTPCode(email=email, otp=otp, expires_at=expires_at)
    db.add(otp_entry)
    db.commit()

def verify_otp(db: Session, email: str, otp: str):
    otp_entry = db.query(OTPCode).filter(
        OTPCode.email == email,
        OTPCode.otp == otp
    ).first()

    if not otp_entry:
        return False, "Invalid OTP"
    
    if datetime.utcnow() > otp_entry.expires_at:
        return False, "OTP expired"
    
    # delete OTP after successful verification
    db.delete(otp_entry)
    db.commit()
    
    return True, "OTP verified"