from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate

async def get_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().all()

async def get_task(db: AsyncSession, task_id: int):
    return await db.get(Task, task_id)

async def create_task(db: AsyncSession, task: TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def update_task(db: AsyncSession, task_id: int, task_update: TaskUpdate):
    db_task = await get_task(db, task_id)
    if not db_task:
        return None
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def delete_task(db: AsyncSession, task_id: int):
    db_task = await get_task(db, task_id)
    if not db_task:
        return None
    await db.delete(db_task)
    await db.commit()
    return db_task
