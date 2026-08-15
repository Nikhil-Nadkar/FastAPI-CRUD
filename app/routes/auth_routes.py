from fastapi import APIRouter, Depends, status
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.controllers.auth_controller import RegisterUser
from app.schemas.user import UserResponse
from app.schemas.auth import TokenResponse, LoginRequest
from app.controllers.auth_controller import LoginUser

router = APIRouter()


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
def registerUser_routes(user: UserCreate, db: Session = Depends(get_db)):
    return RegisterUser(user, db)


@router.post("/login", status_code=200, response_model=TokenResponse)
def loginUser_routes(user_data: LoginRequest, db: Session = Depends(get_db)):
    return LoginUser(user_data, db)
