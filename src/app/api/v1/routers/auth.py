from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

from typing import Annotated
from datetime import timedelta

from src.models.token import Token
from src.models.user import UserGetInfo, UserResponse
from src.utils.jwt import create_access_token
from src.config.constants import settings, db

router = APIRouter(
    prefix="/users"
)

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await db.auth_user(
        username=form_data.username,
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # user[0][0] -> user's UUID
    # user[0][2] -> user's role

    access_token = create_access_token(
        payload_data={
            "sub": str(user[0][0]),
            "role": user[0][2],
        },
        expires_data=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")

@router.post("/register")
async def register(user: UserGetInfo):
    username = user.username
    user_password = user.password
    user_role = user.role

    result = await db.register_new_user(
        username=username,
        role=user_role,
        password=user_password
    )
    print(result)
    if result:
        return {"status": "success"}

    return {"status": "error", "details": "user already exists"}
