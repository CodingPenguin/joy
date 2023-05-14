from fastapi import APIRouter


router = APIRouter()


@router.get("/{user_id}")
async def get_tasks(user_id: str):
    return {}


@router.post("/{user_id}")
async def create_task(user_id: str):
    return {}