from datetime import timedelta
from datetime import datetime
from datetime import timezone

from src.settings import Settings

import jwt

settings = Settings()

def create_access_token(payload_data: dict, expires_data: timedelta) -> str:
    to_encode = payload_data.copy()
    expire = datetime.now(timezone.utc) + expires_data

    to_encode.update(
        {"exp": expire}
    )

    encoded_jwt = jwt.encode(to_encode, settings.SECRET, algorithm="HS256")
    return encoded_jwt


def verify_access_token(token: str) -> dict | None:
    try:
        decoded_jwt = jwt.decode(token, settings.SECRET, algorithms="HS256")
        
        return decoded_jwt
    
    except jwt.InvalidTokenError:
        return None
    
