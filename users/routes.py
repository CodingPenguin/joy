from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from users.models import UserBase, UserCreate


router = APIRouter()


@router.get("/")
async def get_user(request: Request, user: UserBase):
    USERS = request.app.state.mongodb.production.users    
    user = user.dict(exclude_unset=True)

    if (response := await USERS.find_one(user)) is not None:
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)

    return JSONResponse(content=f"NOT ABLE TO FIND USER WITH {user}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/")
async def create_user(request: Request, user: UserCreate):
    USERS = request.app.state.mongodb.production.users    
    user = user.dict(by_alias=True)

    if (await USERS.insert_one(user)) is not None:
        return JSONResponse(content=f"SUCCESS! CREATED USER {user}", status_code=status.HTTP_201_CREATED)

    return JSONResponse(content=f"INVALID INPUT TO CREATE USER {user}", status_code=status.HTTP_406_NOT_ACCEPTABLE)
