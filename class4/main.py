import os
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

# engine 
engine = create_engine(os.getenv("DB_URL"), echo=True)

# how to interact with table

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None =Field(default=None)

def get_session():
    with Session(engine) as session:
        yield session

# how to create table 
def create_tables():
    print("trying to create table")
    SQLModel.metadata.create_all(engine)
    print("table Function Completed")

create_tables()


app = FastAPI()
 
@app.post("/task")
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    return task
