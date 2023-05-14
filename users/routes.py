from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from pymongo import ReturnDocument

from users.models import UserBase, UserCreate, UserUpdate


router = APIRouter()


@router.get("/")
async def get_user(request: Request, user: UserBase):
    USERS = request.app.state.mongodb.production.users    
    user = user.dict(exclude_unset=True, by_alias=True)

    if (response := await USERS.find_one(user)) is not None:
        return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK)

    return JSONResponse(content=user, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/")
async def create_user(request: Request, user: UserCreate):
    USERS = request.app.state.mongodb.production.users    
    user = user.dict(by_alias=True)

    if (response := await USERS.insert_one(user)) is not None:
        inserted_user = await USERS.find_one({"_id": response.inserted_id})
        return JSONResponse(content=jsonable_encoder(inserted_user), status_code=status.HTTP_201_CREATED)

    return JSONResponse(content=user, status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.patch("/{user_id}")
async def update_user(request: Request, user_id: str, user: UserUpdate):
    USERS = request.app.state.mongodb.production.users    
    user = user.dict(exclude_unset=True, by_alias=True)

    if (response := await USERS.find_one_and_update({"_id": user_id}, {"$set": user}, return_document=ReturnDocument.AFTER)) is not None:
        return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK)

    return JSONResponse(content=user_id, status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.delete("/{user_id}")
async def delete_user(request: Request, user_id: str):
    USERS = request.app.state.mongodb.production.users    

    if (await USERS.delete_one({"_id": user_id})) is not None:
        return JSONResponse(content=user_id, status_code=status.HTTP_200_OK)

    return JSONResponse(content=user_id, status_code=status.HTTP_406_NOT_ACCEPTABLE)