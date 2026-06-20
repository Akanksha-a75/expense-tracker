from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, OTPCode
from app.auth.otp import generate_otp, save_otp, verify_otp
from app.auth.smtp import send_otp_email
from app.auth.session import create_token
from app.schemas import SendOTPRequest, VerifyOTPRequest, AuthResponse
from pydantic import BaseModel

router = APIRouter(prefix="/auth")

class SignUpRequest(BaseModel):
    name: str
    email: str

@router.post("/signup")
def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered. Please sign in.")
    
    new_user = User(email=request.email, name=request.name)
    db.add(new_user)
    db.commit()

    otp = generate_otp()
    save_otp(db, request.email, otp)
    send_otp_email(request.email, otp)
    return {"message": "OTP sent to your email."}

@router.post("/send-otp")
def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered. Please sign up first.")
    
    otp = generate_otp()
    save_otp(db, request.email, otp)
    send_otp_email(request.email, otp)
    return {"message": "OTP sent to your email."}

@router.post("/verify-otp", response_model=AuthResponse)
def verify_otp_endpoint(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    valid, message = verify_otp(db, request.email, request.otp)
    if not valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP.")
    
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    token = create_token(request.email)
    return {"message": "Login successful.", "token": token, "email": request.email}