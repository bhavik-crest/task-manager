from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate
from app.database import supabase

async def get_tasks():
    response = supabase.table("tasks").select("*").order("id", desc=True).execute()
    return response.data

async def get_task(task_id: int):
    response = supabase.table("tasks").select("*").eq("id", task_id).execute()
    tasks = response.data
    return tasks[0] if tasks else None

async def create_task(task: TaskCreate):
    response = supabase.table("tasks").insert(task.dict()).execute()
    created_tasks = response.data
    return created_tasks[0] if created_tasks else None

async def update_task(task_id: int, task_update: TaskUpdate):
    update_data = {k: v for k, v in task_update.dict(exclude_unset=True).items()}
    if not update_data:
        return None
    response = supabase.table("tasks").update(update_data).eq("id", task_id).execute()
    updated_tasks = response.data
    return updated_tasks[0] if updated_tasks else None

async def delete_task(task_id: int):
    response = supabase.table("tasks").delete().eq("id", task_id).execute()
    deleted_tasks = response.data
    return deleted_tasks[0] if deleted_tasks else None
