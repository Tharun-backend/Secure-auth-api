from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Temporary database (just for now)
users = []

# User model
class User(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"message": "Secure Auth API is running"}

# Register API
@app.post("/register")
def register(user: User):
    users.append(user)
    return {"message": "User registered successfully"}

# Login API
@app.post("/login")
def login(user: User):
    for u in users:
        if u.username == user.username and u.password == user.password:
            return {"message": "Login successful"}
    return {"message": "Invalid credentials"}