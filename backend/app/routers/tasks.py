from fastapi import APIRouter, HTTPException, status
from app.schemas import Task, TaskCreate, TaskUpdate
from app.crud import get_tasks, get_task, create_task, update_task, delete_task

router = APIRouter()

@router.get("/tasks", response_model=list[Task])
async def read_tasks():
    try:
        return await get_tasks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    try:
        task = await get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def add_task(task: TaskCreate):
    try:
        return await create_task(task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasks/{task_id}", response_model=Task)
async def edit_task(task_id: int, task_update: TaskUpdate):
    try:
        updated_task = await update_task(task_id, task_update)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tasks/{task_id}", response_model=Task)
async def remove_task(task_id: int):
    try:
        deleted_task = await delete_task(task_id)
        if not deleted_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return deleted_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))