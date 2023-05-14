from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from pymongo import ReturnDocument

from tasks.models import TaskBase, TaskCreate, TaskUpdate


router = APIRouter()


@router.get("/")
async def get_tasks(request: Request, task_query: TaskBase):
    TASKS = request.app.state.mongodb.production.tasks   
    TASK_LIMIT = 99 
    task_query = task_query.dict(exclude_unset=True, by_alias=True)
    
    if (response := await TASKS.find(task_query).to_list(length=TASK_LIMIT)) is not None:
        return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/{user_id}")
async def create_task(request: Request, user_id: str, task: TaskCreate):
    # CHECK IF USER EXISTS WITH USER_ID?!
    TASKS = request.app.state.mongodb.production.tasks    
    task.user_id = user_id
    task = task.dict(by_alias=True)

    if (response := await TASKS.insert_one(task)) is not None:
        inserted_task = await TASKS.find_one({"_id": response.inserted_id})
        return JSONResponse(content=jsonable_encoder(inserted_task), status_code=status.HTTP_201_CREATED)

    return JSONResponse(content=task, status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.patch("/{task_id}")
async def update_task(request: Request, task_id: str, task: TaskUpdate):
    # TODO: will have to do logic to level up user... find the algo!
    TASKS = request.app.state.mongodb.production.tasks    
    task = task.dict(exclude_unset=True, by_alias=True)
    print(task)

    if (response := await TASKS.find_one_and_update({"_id": task_id}, {"$set": task}, return_document=ReturnDocument.AFTER)) is not None:
        return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK)

    return JSONResponse(content=task_id, status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.delete("/{task_id}")
async def delete_task(request: Request, task_id: str):
    TASKS = request.app.state.mongodb.production.tasks    

    if (await TASKS.delete_one({"_id": task_id})) is not None:
        return JSONResponse(content=task_id, status_code=status.HTTP_200_OK)

    return JSONResponse(content=task_id, status_code=status.HTTP_406_NOT_ACCEPTABLE)