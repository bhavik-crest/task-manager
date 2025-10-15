from pydantic import BaseModel, validator, root_validator
from typing import Optional, Literal

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = ""
    status: Literal["pending", "done"] = "pending"

    @validator('title')
    def title_length(cls, v):
        if not (1 <= len(v) <= 100):
            raise ValueError('Title must be between 1 and 100 characters')
        return v

    @validator('description')
    def description_length(cls, v):
        if v and len(v) > 300:
            raise ValueError('Description must be at most 300 characters')
        return v

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[Literal["pending", "done"]]

    @validator('title')
    def title_length(cls, v):
        if v is not None:
            if len(v.strip()) == 0 or not (1 <= len(v) <= 100):
                raise ValueError('Title must be between 1 and 100 characters and not empty')
        return v

    @validator('description')
    def description_length(cls, v):
        if v is not None and len(v) > 300:
            raise ValueError('Description must be at most 300 characters')
        return v


class TaskOut(TaskBase):
    id: int

    class Config:
        orm_mode = True
