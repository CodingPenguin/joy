import os, motor
from fastapi import FastAPI


app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.production


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users")
async def users_get():
    return {}


@app.get("/tasks/{user_id}")
async def tasks_get(user_id: str):
    return {}


@app.post("/tasks/{user_id}")
async def tasks_post(user_id: str):
    return {}