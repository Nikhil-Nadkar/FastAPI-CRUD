from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import hash_password, verfiy_password
from fastapi import HTTPException, status
from app.utils.jwt_helper import create_access_token


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


def LoginUser(user_data: LoginRequest, db: Session):

    user = db.query(User).filter(User.email == user_data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    if verfiy_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    token = create_access_token(user.id)

    return {"access_token": token, "token_type": "bearer"}
