# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime

# ----------- User -----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

# ----------- Stage -----------
class StageCreate(BaseModel):
    name: str

class StageOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True

# ----------- Task -----------
class TaskCreate(BaseModel):
    title: str

class TaskOut(BaseModel):
    id: int
    title: str
    is_archived: bool
    stages: List[StageOut] = []

    class Config:
        orm_mode = True
