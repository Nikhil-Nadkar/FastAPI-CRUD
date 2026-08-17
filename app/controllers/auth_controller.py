from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest, RefreshTokenRequest
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import hash_password, verfiy_password
from fastapi import HTTPException, status
from app.utils.jwt_helper import create_access_token, create_refresh_token
import jwt
from app.config.settings import settings


def RegisterUser(user: UserCreate, db: Session):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email already Registered"
        )

    hashpassword = hash_password(user.password)

    newUser = User(name=user.name, email=user.email, password=hashpassword)

    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser


# def LoginUser(user_data: LoginRequest, db: Session):

#     user = db.query(User).filter(User.email == user_data.email).first()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
#         )

#     if verfiy_password(user_data.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
#         )

#     token = create_access_token(user.id)

#     return {"access_token": token, "token_type": "bearer"}


def LoginUser(email: str, password: str, db: Session):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    if not verfiy_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password wrong",
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def refresh_access_token(refreshToken: str, db: Session):
    try:
        payload = jwt.decode(
            refreshToken, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )

        user_id = payload.get("sub")
        token_type = payload.get("type")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token01",
            )

        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token02",
            )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token02"
        )

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    new_access_token = create_access_token(user.id)

    return new_access_token
