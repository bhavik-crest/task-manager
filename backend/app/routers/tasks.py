from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import Task, TaskCreate, TaskUpdate
from app.crud import get_tasks, get_task, create_task, update_task, delete_task
from app.database import get_db

router = APIRouter()

@router.get("/tasks", response_model=list[Task])
async def read_tasks(db: AsyncSession = Depends(get_db)):
    return await get_tasks(db)

@router.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def add_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await create_task(db, task)

@router.post("/tasks/{task_id}", response_model=Task)
async def edit_task(task_id: int, task_update: TaskUpdate, db: AsyncSession = Depends(get_db)):
    updated_task = await update_task(db, task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/tasks/{task_id}", response_model=Task)
async def remove_task(task_id: int, db: AsyncSession = Depends(get_db)):
    deleted_task = await delete_task(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task
