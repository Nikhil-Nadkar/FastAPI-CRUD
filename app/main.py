from fastapi import FastAPI

from app.database.database import Base, engine
from app.models import user
from app.routes import user_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def home():
  return {"message": "Heloo FastAPI"}

app.include_router(user_routes.router, prefix="/user")