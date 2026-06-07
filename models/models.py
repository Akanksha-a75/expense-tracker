from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class User:
    """User model for storing user information"""
    name: str
    phone: str
    email: str
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }


@dataclass
class OTP:
    """OTP model for storing OTP information"""
    email: str
    otp_code: str
    created_at: datetime = field(default_factory=datetime.now)
    is_verified: bool = False
    id: Optional[int] = None
    expires_at: Optional[datetime] = None

    def is_expired(self):
        """Check if OTP has expired"""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "otp_code": self.otp_code,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "expires_at": self.expires_at.isoformat() if isinstance(self.expires_at, datetime) else self.expires_at,
            "is_verified": self.is_verified
        }


@dataclass
class Expense:
    """Expense model for storing expense information"""
    user_id: int
    amount: float
    category: str
    expense_date: datetime
    id: Optional[int] = None
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "expense_date": self.expense_date.isoformat() if isinstance(self.expense_date, datetime) else self.expense_date,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
