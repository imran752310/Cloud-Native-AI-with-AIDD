from fastapi import FastAPI
from app.api.routes import users, tasks
from app.db.init_db import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(users.router)
app.include_router(tasks.router)