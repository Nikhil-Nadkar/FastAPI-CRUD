from fastapi import APIRouter, Depends, status
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.schemas.user import UserResponse
from app.schemas.auth import TokenResponse, LoginRequest, RefreshTokenRequest
from app.controllers.auth_controller import (
    LoginUser,
    refresh_access_token,
    RegisterUser,
)
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
def registerUser_routes(user: UserCreate, db: Session = Depends(get_db)):
    return RegisterUser(user, db)


@router.post("/login", status_code=200, response_model=TokenResponse)
def loginUser_routes(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return LoginUser(form_data.username, form_data.password, db)


@router.post("/refresh")
def refreshToken_routes(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    return refresh_access_token(data.refresh_token, db)
