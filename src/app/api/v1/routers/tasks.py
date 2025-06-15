from uuid import uuid4

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.exceptions import HTTPException

from pydantic import UUID4, Json
from typing import Optional

from src.models.task import TaskGet

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

@router.get("/get_task/{id}")
async def get_task(id: UUID4, token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_role = await db.get_role_by_id(user_id)
        tasks_owner = await db.get_task_by_id(id)


        if user_role[0][0] == "user" and str(tasks_owner[0][0]) == user_id:
            result = await db.get_task_by_id(id)

            if result:
                return {"result": result}
            else:
                return {"status": "error"}
        else:
            return None

    except Exception as err:
        raise Exception(err)

@router.delete("/delete_task/{id}")
async def delete_task(id: UUID4, token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_role = await db.get_role_by_id(user_id)
        tasks_owner = await db.get_task_by_id(id)

        if (user_role[0][0] == "user" and str(tasks_owner[0][0]) == user_id) \
                or (user_role[0][0] == "admin"):
            result = await db.delete_task_by_id(id)

            if result:
                return {"result": result}
            else:
                return {"status": "error"}
        else:
            return None

    except Exception as err:
        raise Exception(err)

@router.get("/get_all")
async def get_tasks(status: Optional[str] = None,
                    user: Optional[str] = None,
                    date: Optional[float] = None,
                    token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_role = await db.get_role_by_id(user_id)

        if user_role[0][0] == "admin":
            result = await db.sort_tasks(status, user, date)

            if result:
                return {"result": result}
            else:
                return {"status": "error"}
        else:
            return None

    except Exception as err:
        raise Exception(err)

@router.put("/update/{id}")
async def update_task(id: UUID4,
                    title: Optional[str] = None,
                    description: Optional[str] = None,
                    status: Optional[str] = None,
                    created_at: Optional[float] = None,
                    city: Optional[str] = None,
                    weather: Optional[Json] = None,
                    token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_role = await db.get_role_by_id(user_id)

        if user_role[0][0] == "admin":
            result = await db.update_task_by_id(
                id, title, description, status, created_at, city, weather
            )
            if result:
                return {"result": result}
            else:
                return {"status": "error"}
        else:
            return None

    except Exception as err:
        raise Exception(err)