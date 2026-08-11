from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers.user_controllers import get_users
from app.database.database import get_db

router = APIRouter()

@router.get('/')
def get_all_users(
  db: Session = Depends(get_db)
):
  return get_users(db)