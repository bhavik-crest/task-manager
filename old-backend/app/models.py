from sqlalchemy import Column, Integer, String, Enum
from app.database import Base

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(Enum('pending', 'done', name='task_status'), default='pending', nullable=False)
