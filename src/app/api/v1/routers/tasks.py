from uuid import uuid4

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.exceptions import HTTPException

from src.models.token import Token
from src.models.task import TaskGet, TaskResponse

from src.utils.jwt import verify_access_token
from src.config.constants import db, oauth2_scheme

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.post("/create_task")
async def create_task_api(task: TaskGet, token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        task_id = uuid4()
        result = await db.create_task(
            id=task_id,
            user_id=user_id,
            title=task.title,
            description=task.description,
            status=task.status,
            created_at=task.created_at,
            city=task.city,
            weather=task.weather
        )

        if result:
            return result
        else:
            raise HTTPException(status_code=400, detail="Failed to create task")

    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail="Internal server error")
