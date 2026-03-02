import os
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
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
 
@app.post("/tasks")
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.get("/tasks")
def get_task(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()   
    return tasks

# get single record 
@app.get("/tasks/{task_id}")
def get_task(task_id: int, session:Session = Depends(get_session)):
    task = session.get(Task, task_id)
    return task

# delete record 

# DELETE
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted", "id": task_id}

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_data: Task,
    session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_data.title
    task.description = task_data.description
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
