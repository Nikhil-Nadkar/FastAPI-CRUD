from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers.user_controllers import (
    get_users,
    create_user,
    get_single_user,
    delete_user,
    update_user,
)
from app.database.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.models.user import User
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.post("/", status_code=201, response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)


@router.get("/{user_id}", response_model=UserResponse)
def get_single_user_routes(user_id: int, db: Session = Depends(get_db)):
    return get_single_user(user_id, db)


@router.delete("/{user_id}")
def delete_user_routes(user_id: int, db: Session = Depends(get_db)):
    return delete_user(user_id, db)


@router.put("/{user_id}", response_model=UserUpdate)
def update_user_routes(user: UserCreate, user_id: int, db: Session = Depends(get_db)):
    return update_user(user, user_id, db)
