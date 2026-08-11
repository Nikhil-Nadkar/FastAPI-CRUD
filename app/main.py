from fastapi import FastAPI
from app.routes import user_routes

app = FastAPI()

@app.get('/')
def home():
  return {"message": "Heloo FastAPI"}

app.include_router(user_routes.router, prefix="/user")