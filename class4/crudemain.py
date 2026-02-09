from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task API")

# Models
class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    status: str | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str

# Storage
tasks: list[dict] = []
task_counter = 0

# CREATE
@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    global task_counter
    task_counter += 1
    new_task = {
        "id": task_counter,
        "title": task.title,
        "description": task.description,
        "status": "pending"
    }
    tasks.append(new_task)
    return new_task

# READ (all)
@app.get("/tasks")
def list_tasks(status: str | None = None):
    if status:
        return [t for t in tasks if t["status"] == status]
    return tasks

# READ (one)
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# UPDATE
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = task_update.title
            if task_update.description is not None:
                task["description"] = task_update.description
            if task_update.status is not None:
                task["status"] = task_update.status
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# DELETE
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return {"message": "Task deleted", "id": task_id}
    raise HTTPException(status_code=404, detail="Task not found")