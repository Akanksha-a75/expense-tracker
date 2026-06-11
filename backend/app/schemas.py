from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date as date_type

class SendOTPRequest(BaseModel):
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str

class AuthResponse(BaseModel):
    message: str
    token: str = None


    

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    date: date_type
    description: Optional[str] = None

class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    date: date_type
    description: Optional[str] = None

    class Config:
        from_attributes = True