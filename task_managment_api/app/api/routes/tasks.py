from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead
from app.api.deps import db_session

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, session: Session = Depends(db_session)):
    db_task = Task(title=task.title, user_id=task.user_id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/", response_model=list[TaskRead])
def get_tasks(session: Session = Depends(db_session)):
    return session.exec(select(Task)).all()

@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(db_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"message": "Task deleted"}