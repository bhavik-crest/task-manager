from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from . import models, schemas


def get_tasks(db: Session):
    try:
        return db.query(models.Task).all()
    except SQLAlchemyError as e:
        print(f"[ERROR] Failed to fetch tasks: {e}")
        return []


def get_task(db: Session, task_id: int):
    try:
        return db.query(models.Task).filter(models.Task.id == task_id).first()
    except SQLAlchemyError as e:
        print(f"[ERROR] Failed to fetch task with id {task_id}: {e}")
        return None


def create_task(db: Session, task: schemas.TaskCreate):
    try:
        db_task = models.Task(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[ERROR] Failed to create task: {e}")
        return None


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    try:
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if db_task is None:
            print(f"[INFO] Task with id {task_id} not found for update.")
            return None

        for key, value in task.dict(exclude_unset=True).items():
            setattr(db_task, key, value)

        db.commit()
        db.refresh(db_task)
        return db_task
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[ERROR] Failed to update task with id {task_id}: {e}")
        return None


def delete_task(db: Session, task_id: int):
    try:
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if db_task is None:
            print(f"[INFO] Task with id {task_id} not found for deletion.")
            return None

        db.delete(db_task)
        db.commit()
        return db_task
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[ERROR] Failed to delete task with id {task_id}: {e}")
        return None