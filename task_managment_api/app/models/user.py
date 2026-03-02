from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr = Field(unique=True, index=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)