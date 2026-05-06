from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = []

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
    users.append({"username": user.username, "password": hashed_pwd})
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: User):
    for u in users:
        if u["username"] == user.username and verify_password(user.password, u["password"]):
            token = create_token({"sub": user.username})
            return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Protected route
@app.get("/protected")
def protected(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"message": f"Welcome {payload['sub']}"}
    except:
        raise HTTPException(status_code=401, detail="Invalid token")