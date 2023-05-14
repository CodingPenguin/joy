import os
from dotenv import load_dotenv
from loguru import logger

from fastapi import FastAPI

from tasks.routes import router as tasks_router
from users.routes import router as users_router

from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv()

# ----------- LOAD ROUTERS ----------- #
app = FastAPI()
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
app.include_router(users_router, prefix="/users", tags=["users"])


# ----------- DATABASE CONNECTION ----------- #
async def open_db() -> AsyncIOMotorClient:
    app.state.mongodb = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    logger.info("CONNECTED TO MONGODB!")


async def close_db():
    app.state.mongodb.close()
    logger.info("CLOSED MONGODB!")


app.add_event_handler("startup", open_db)
app.add_event_handler("shutdown", close_db)