from pydantic import UUID4, BaseModel
from src.models.enums.role_enums import Role

class UserResponse(BaseModel):
    id: UUID4
    username: str
    role: Role
    password_hash: str

class UserGetInfo(BaseModel):
    username: str
    role: Role
    password: str