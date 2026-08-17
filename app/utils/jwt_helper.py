from datetime import datetime, timezone, timedelta
import jwt
from app.config.settings import settings


def create_token(user_id: int, expire_time: timedelta, token_type: str):
    expire = datetime.now(timezone.utc) + expire_time

    payload = {"sub": str(user_id), "exp": expire, "type": token_type}

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(user_id: int):

    return create_token(
        user_id, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY), "access"
    )


def create_refresh_token(user_id: int):
    return create_token(
        user_id, timedelta(days=settings.REFRESH_TOKEN_EXPIRY), "refresh"
    )
