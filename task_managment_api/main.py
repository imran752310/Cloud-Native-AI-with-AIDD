from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List

app =FastAPI()

class Todo(BaseModel):
    id: int
    title: str
    description: str

# memory 
todos : Dict[int, Todo] ={}

# craete 
@app.post("/")
def create_todos(todo: Todo):
    todos[todo.id] = todo
    return todo

@app.get("/todo")
def get_todos():
    return list(todos.values())

@app.get("/todo/{todo_id}")
def get_onetodo(todo_id: int):
    return todos.get(todo_id)

@app.put("/todo/{todo_id}")
def update_todo(todo_id: int, todo:Todo):
    todos[todo_id] = todo
    return todo

@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int):
    del todos[todo_id]
    return {"message ": "item delete ok" }


