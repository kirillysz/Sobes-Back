from pydantic import UUID4, BaseModel, Json
from typing import Optional, Dict, Any

from src.models.enums.status_enums import Status

class TaskResponse(BaseModel):
    id: UUID4
    user_id: int
    title: str
    description: str
    status: Status
    created_at: float
    city: Optional[str]
    weather: Optional[Dict[str, Any]]


class TaskGet(BaseModel):
    title: str
    description: str
    status: Status
    created_at: float
    city: Optional[str] = None
    weather: Optional[Dict[str, Any]] = None