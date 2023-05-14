from uuid import uuid4
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Literal

from helpers.time_format import date_to_str


STATE_VALUES = Literal["completed", "uncompleted"]


class TaskBase(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: Optional[str] = Field(alias="userId")
    created_at: Optional[datetime] = Field(alias="createdAt")
    scheduled_at: Optional[datetime] = Field(alias="scheduledAt")
    description: Optional[str]
    state: Optional[STATE_VALUES]
    points: Optional[int]


class TaskCreate(TaskBase):
    id: Optional[str] = Field(alias="_id", default=str(uuid4()))
    created_at: Optional[datetime] = Field(alias="createdAt", default=date_to_str(datetime.utcnow()))
    scheduled_at: datetime = Field(alias="scheduledAt")
    state: STATE_VALUES
    points: int


class TaskUpdate(TaskBase):
    description: Optional[str]
    state: Optional[STATE_VALUES]


class TaskDelete(BaseModel):
    # not inherited !!!
    id: str = Field(alias="_id")
