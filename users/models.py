from uuid import uuid4
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal


RANK_VALUES = Literal["bronze", "silver", "gold", "platinum", "diamond", "champion", "legend"]


class UserBase(BaseModel):
    id: Optional[str] = Field(alias="_id")
    created_at: Optional[datetime] = Field(alias="createdAt")
    username: Optional[str]
    bio: Optional[str]
    rank: Optional[RANK_VALUES]
    xp: Optional[int]


class UserCreate(UserBase):
    id: Optional[str] = Field(alias="_id", default=str(uuid4()))
    created_at: Optional[datetime] = Field(alias="createdAt", default=datetime.utcnow())
    username: str
    rank: RANK_VALUES = Field(default="bronze")
    xp: int = Field(default=0)


class UserUpdate(UserBase):
    bio: Optional[str]
    rank: Optional[int]
    xp: Optional[int]