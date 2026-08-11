from fastapi import APIRouter
from app.controllers.user_controllers import get_users

router = APIRouter()

@router.get('/')
def get_all_users():
  return get_users()