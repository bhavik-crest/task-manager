from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate


async def get_tasks(db: AsyncSession):
    try:
        result = await db.execute(select(Task))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred when fetching tasks.")


async def get_task(db: AsyncSession, task_id: int):
    try:
        return await db.get(Task, task_id)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred when fetching task.")


async def create_task(db: AsyncSession, task: TaskCreate):
    db_task = Task(**task.dict())
    try:
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Task already exists or violates constraints.")
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred when creating task.")


async def update_task(db: AsyncSession, task_id: int, task_update: TaskUpdate):
    try:
        db_task = await get_task(db, task_id)
        if not db_task:
            return None
        for key, value in task_update.dict(exclude_unset=True).items():
            setattr(db_task, key, value)
        await db.commit()
        await db.refresh(db_task)
        return db_task
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred when updating task.")


async def delete_task(db: AsyncSession, task_id: int):
    try:
        db_task = await get_task(db, task_id)
        if not db_task:
            return None
        await db.delete(db_task)
        await db.commit()
        return db_task
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred when deleting task.")
