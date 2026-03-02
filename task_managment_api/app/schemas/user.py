from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime

class UserCreate(SQLModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)  # ✅ IMPORTANT

class UserRead(SQLModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

class UserLogin(SQLModel):
    email: str
    password: str