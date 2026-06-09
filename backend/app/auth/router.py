from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth.otp import generate_otp, save_otp, verify_otp
from app.auth.smtp import send_otp_email
from app.auth.session import create_token
from app.schemas import SendOTPRequest, VerifyOTPRequest, AuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/send-otp", response_model=AuthResponse)
def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    email = request.email

    # create user if doesn't exist
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email)
        db.add(user)
        db.commit()

    otp = generate_otp()
    save_otp(db, email, otp)
    send_otp_email(email, otp)

    return {"message": "OTP sent successfully"}


@router.post("/verify-otp", response_model=AuthResponse)
def verify_otp_route(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    success, message = verify_otp(db, request.email, request.otp)

    if not success:
        raise HTTPException(status_code=400, detail=message)

    token = create_token(request.email)
    return {"message": "Login successful", "token": token}