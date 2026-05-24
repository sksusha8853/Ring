from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Request/Response Models

class UserSignup(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    phone: str
    whatsapp: str
    instructions: str = Field(default="", max_length=500)

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    instructions: Optional[str] = Field(None, max_length=500)

class UserResponse(BaseModel):
    username: str
    phone: str
    whatsapp: str
    instructions: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    profile_url: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class PublicProfileResponse(BaseModel):
    username: str
    phone: str
    whatsapp: str
    instructions: str
    updated_at: Optional[datetime] = None

class ErrorResponse(BaseModel):
    detail: str

# MongoDB Document Models (for reference)
"""
User Document Structure:
{
    "_id": ObjectId,
    "username": "john_doe",  # unique
    "email": "john@example.com",  # unique (optional for future)
    "password_hash": "hashed_password",
    "phone": "+1234567890",
    "whatsapp": "+1234567890",
    "instructions": "Available 9AM-5PM",
    "created_at": datetime,
    "updated_at": datetime
}

Visit Document Structure (for analytics):
{
    "_id": ObjectId,
    "username": "john_doe",
    "ip_address": "192.168.1.1",
    "user_agent": "Mozilla/5.0...",
    "timestamp": datetime
}
"""
