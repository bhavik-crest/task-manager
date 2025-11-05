# app/schemas.py

from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional
from enum import Enum


class StatusEnum(str, Enum):
    pending = "pending"
    done = "done"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Title is required and must be between 1 and 100 characters")
    description: Optional[str] = Field(None, max_length=500, description="Optional description up to 500 characters")
    status: StatusEnum = StatusEnum.pending

    model_config = ConfigDict(from_attributes=True, validate_assignment=True)

    @validator('title')
    def title_cannot_be_blank(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or blank spaces')
        return v


class TaskCreate(TaskBase):
    title: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.pending

    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[StatusEnum] = None

    model_config = ConfigDict(from_attributes=True, validate_assignment=True)

    @validator('title')
    def title_if_present_not_blank(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty or blank spaces')
        return v


class Task(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
