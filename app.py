from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Dict

app = FastAPI(
    title="User Management API",
    description="A simple FastAPI app for managing users (in-memory)",
    version="1.0.0"
)

# Simple in-memory database
users_db: Dict[int, dict] = {}


# User schema
class User(BaseModel):
    id: int
    name: str
    email: EmailStr  # validates proper email format


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Welcome to the FastAPI User Service!"}


# Create a new user
@app.post("/users/", status_code=201)
def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail=f"User with ID {user.id} already exists.")
    
    users_db[user.id] = user.dict()
    return {
        "message": "User created successfully",
        "user": user
    }


# Get user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    return user


# Update user
@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    
    users_db[user_id] = updated_user.dict()
    return {
        "message": "User updated successfully",
        "user": updated_user
    }


# Delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    
    del users_db[user_id]
    return {"message": f"User with ID {user_id} deleted successfully."}
