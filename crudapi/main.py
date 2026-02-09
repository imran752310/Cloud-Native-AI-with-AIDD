from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

class Todo(BaseModel):
    id: int
    task: str
    description: str

# memnory
alltodos: Dict[int, list] = {}

@app.post("/")
def create_todo(todo: Todo):
    alltodos[todo.id] = todo
    return todo

@app.get("/")
def get_todos():
    return list(alltodos.values())

@app.get("/todo/{todo_id}")
def getoneTodo(todo_id : int):
   return  alltodos.get(todo_id)
    
@app.put("/todo/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    alltodos[todo_id] = todo
    return todo

@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int):
    del alltodos[todo_id]
    return {"message " : "delete onk"}

        