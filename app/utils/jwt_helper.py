from datetime import datetime, timezone, timedelta
import jwt
from app.config.settings import settings


def create_access_token(user_id: int):

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.TOKEN_EXPIRY)

    payload = {"sub": str(user_id), "exp": expire}

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return token
