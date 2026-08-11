from app.models.user import User
from sqlalchemy.orm import Session

def get_users(db:Session):
    user = db.query(User).all()
    return {'message' : "got all users", 'users': user}