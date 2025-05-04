# app/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.db import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    new_task = models.Task(title=task.title, user_id=user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=list[schemas.TaskOut])
def list_tasks(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Task).filter_by(user_id=user.id, is_archived=False).all()

@router.get("/all", response_model=list[schemas.TaskOut])  # ✅ Добавлено
def list_all_tasks(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Task).filter_by(user_id=user.id).all()

@router.patch("/{task_id}/archive")
def archive_task(task_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter_by(id=task_id, user_id=user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.is_archived = True
    db.commit()
    return {"msg": "Task archived"}

@router.post("/{task_id}/stages")
def add_stage(task_id: int, stage: schemas.StageCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter_by(id=task_id, user_id=user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    new_stage = models.Stage(task_id=task.id, name=stage.name)
    db.add(new_stage)
    db.commit()
    return {"msg": "Stage added"}
