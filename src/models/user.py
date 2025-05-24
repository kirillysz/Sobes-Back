from pydantic import UUID4, BaseModel
from src.models.enums.role_enums import Role

class User(BaseModel):
    id: UUID4
    username: str
    role: Role
    password_hash: str
