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
from app.schemas.user import UserCreate

router = APIRouter()


@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.post("/")
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)


@router.get("/{user_id}")
def get_single_user_routes(user_id: int, db: Session = Depends(get_db)):
    return get_single_user(user_id, db)


@router.delete("/{user_id}")
def delete_user_routes(user_id: int, db: Session = Depends(get_db)):
    return delete_user(user_id, db)


@router.put("/{user_id}")
def update_user_routes(user: UserCreate, user_id: int, db: Session = Depends(get_db)):
    return update_user(user, user_id, db)
