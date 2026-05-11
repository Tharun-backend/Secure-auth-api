from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy import text
from database import engine

app = FastAPI()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    password: str

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/register")
def register(user: User):
    hashed_pwd = hash_password(user.password)

    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO users (username, password) VALUES (:username, :password)"),
            {"username": user.username, "password": hashed_pwd}
        )
        conn.commit()

    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: User):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM users WHERE username=:username"),
            {"username": user.username}
        ).fetchone()

    if result and verify_password(user.password, result[2]):
        token = create_token({"sub": user.username})
        return {"access_token": token}

    raise HTTPException(status_code=401, detail="Invalid credentials")