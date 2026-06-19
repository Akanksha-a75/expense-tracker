from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class OTPVerification(Base):
    __tablename__ = "otp_verifications"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    otp = Column(String(10), nullable=False)
    is_verified = Column(String(10), default="False")
    created_at = Column(DateTime, default=datetime.utcnow)

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)

    amount = Column(Integer, nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(String(255))

    created_at = Column(DateTime, default=datetime.utcnow)