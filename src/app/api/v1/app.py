from fastapi import FastAPI

from src.app.api.v1.routers import auth
from src.app.api.v1.routers import tasks
from src.config.constants import db_init

app = FastAPI(
    description="Task's API"
)

@app.on_event("startup")
async def init():
    await db_init.create_tables()

app.include_router(
    auth.router
)

app.include_router(
    tasks.router
)