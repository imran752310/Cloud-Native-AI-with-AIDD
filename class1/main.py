from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title = "this is simple test",
    description = "hi"
)



class UserCreate(BaseModel):
    name: str
    email: str
    age: int

@app.get("/")
def root():
    return {
        "message" : "Hello world",
    }
@app.post("/users")
def create_user(user: UserCreate):
    return {
        "id": 1,
        "name": user.name,
        "email": user.email
    }