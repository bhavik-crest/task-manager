from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import Task, TaskCreate, TaskUpdate
# from app.crud import get_tasks, get_task, create_task, update_task, delete_task
from app.database import get_db

router = APIRouter()

@app.get("/health")
async def health():
    return {"status": "okkkkk"}
    
@router.get("/tasks", response_model=list[Task])
async def read_tasks(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Task))
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    try:
        task = await db.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def add_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_task = Task(**task.dict())
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasks/{task_id}", response_model=Task)
async def edit_task(task_id: int, task_update: TaskUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated_task = await get_task(db, task_id)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        for key, value in task_update.dict(exclude_unset=True).items():
            setattr(updated_task, key, value)
        await db.commit()
        await db.refresh(updated_task)
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tasks/{task_id}", response_model=Task)
async def remove_task(task_id: int, db: AsyncSession = Depends(get_db)):
    try:
        deleted_task = await delete_task(db, task_id)
        if not deleted_task:
            raise HTTPException(status_code=404, detail="Task not found")
        await db.delete(db_task)
        await db.commit()
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))