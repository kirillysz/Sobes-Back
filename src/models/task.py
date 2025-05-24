from pydantic import UUID4, BaseModel, Json
from typing import Optional

from datetime import datetime

from src.models.enums.status_enums import Status

class Task(BaseModel):
    id: UUID4
    user_id: int
    title: str
    description: str
    status: Status
    created_at: datetime = datetime.now().timestamp()
    city: Optional[str]
    weather: Optional[Json]

