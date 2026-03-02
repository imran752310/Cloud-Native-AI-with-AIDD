from sqlmodel import SQLModel
from datetime import datetime

class TaskCreate(SQLModel):
    title: str
    user_id: int


class TaskRead(SQLModel):
    id: int
    title: str
    completed: bool
    user_id: int         
    created_at: datetime