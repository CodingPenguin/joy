from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Literal

class TaskBase(BaseModel):
    id: str = Field(alias="_id")
    user_id: str = Field(alias="userId")
    created_at: datetime = Field(alias="createdAt", default=datetime.utcnow())
    description: Optional[str] = Field(default="")
    state: List[Literal["completed", "uncompleted"]] = "uncompleted"
    points: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    description: Optional[str]
    state: Optional[List[Literal["completed", "uncompleted"]]]


class TaskDelete(BaseModel):
    # not inherited !!!
    id: str = Field(alias="_id")
