from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate
from sqlalchemy.exc import SQLAlchemyError

async def get_tasks(db: AsyncSession):
    try:
        result = await db.execute(select(Task))
        return result.scalars().all()
    except SQLAlchemyError as e:
        # Log or process DB errors specially if required
        raise

async def get_task(db: AsyncSession, task_id: int):
    try:
        return await db.get(Task, task_id)
    except SQLAlchemyError as e:
        raise

async def create_task(db: AsyncSession, task: TaskCreate):
    try:
        db_task = Task(**task.dict())
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task
    except SQLAlchemyError as e:
        await db.rollback()
        raise

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
    except SQLAlchemyError as e:
        await db.rollback()
        raise

async def delete_task(db: AsyncSession, task_id: int):
    try:
        db_task = await get_task(db, task_id)
        if not db_task:
            return None
        await db.delete(db_task)
        await db.commit()
        return db_task
    except SQLAlchemyError as e:
        await db.rollback()
        raise