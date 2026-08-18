from sqlalchemy import Column, Integer, String, DateTime
from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(
        String,
        unique=True,
        index=True,
    )
    password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)
    created_at = Column(DateTime, nullable=True)
