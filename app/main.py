# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import get_db, engine
from app.models import Base
from app.schemas import UserCreate, UserOut
from app.auth import create_user, authenticate_user, create_access_token
from app.tasks import router as tasks_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(tasks_router)

@app.post("/auth/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user.email, user.password)
    return new_user

@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}
