from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Literal

class UserBase(BaseModel):
    id: str = Field(alias="_id")
    created_at: datetime = Field(alias="createdAt", default=datetime.utcnow())
    username: str
    bio: Optional[str]


class UserCreate(UserBase):
    rank: List[Literal["bronze", "silver", "gold", "platinum", "diamond", "champion", "legend"]] = Field(default="bronze")
    xp: int = Field(default=0)


class UserUpdate(UserBase):
    bio: Optional[str]
    rank: Optional[int]
    xp: Optional[int]


class UserDelete(BaseModel):
    # not inherited !!!
    id: str = Field(alias="_id")
