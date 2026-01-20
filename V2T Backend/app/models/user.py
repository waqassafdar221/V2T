from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

Base = declarative_base()


class UserRole(str, Enum):
    """User role enumeration."""
    STUDENT = "Student"
    TEACHER = "Teacher"
    OTHERS = "Others"


class User(Base):
    """User database model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OTPCode(Base):
    """OTP verification code database model."""
    __tablename__ = "otp_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    code = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)


# Pydantic models for API
class UserSignup(BaseModel):
    """User signup request model."""
    name: str = Field(..., min_length=2, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: UserRole
    password: str = Field(..., min_length=8, max_length=100)


class VerifyOTP(BaseModel):
    """OTP verification request model."""
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)


class UserLogin(BaseModel):
    """User login request model."""
    username_or_email: str
    password: str


class UserResponse(BaseModel):
    """User response model."""
    id: int
    name: str
    username: str
    email: str
    role: str
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Updated for Pydantic V2


class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    """Token data model."""
    username: Optional[str] = None
