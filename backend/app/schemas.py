from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    pending = "pending"
    done = "done"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.pending

    model_config = ConfigDict(from_attributes=True)

class TaskCreate(TaskBase):
    title: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.pending

    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None

    model_config = ConfigDict(from_attributes=True)

class Task(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)