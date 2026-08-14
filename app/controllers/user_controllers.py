from app.models.user import User
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.utils.security import hash_password


# get all users
def get_users(db: Session):
    return db.query(User).all()
    # return {"message": "got all users", "users": user}


# create new user
def create_user(user: UserCreate, db: Session):
    hashed_password = hash_password(user.password)

    newuser = User(name=user.name, email=user.email, password=hashed_password)

    try:
        db.add(newuser)
        db.commit()
        db.refresh(newuser)

        return newuser

    except IntegrityError:
        db.rollback()

        raise HTTPException(status_code=409, detail="Email already exists")


# get user by id
def get_single_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return user


# update user by id
def update_user(user: UserUpdate, user_id: int, db: Session):
    getuser = db.query(User).filter(User.id == user_id).first()

    if not getuser:
        raise HTTPException(status_code=404, detail={"user not found"})

    getuser.name = user.name
    getuser.email = user.email

    try:
        db.commit()
        db.refresh(getuser)

        return getuser
    except IntegrityError:
        db.rollback()

        raise HTTPException(status_code=409, detail="Email already exists")


# delete user by id
def delete_user(user_id: int, db: Session):
    user = db.query(User).filter(user_id == User.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "user deleted", "user_id": user_id}
