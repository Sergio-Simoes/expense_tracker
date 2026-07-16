from fastapi import FastAPI
from app.database import engine, Base

from app.users import models as user_models
from app.users import router as user_router
from app.expenses import models as expense_models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    user_router.router
)

@app.get("/")
def home():
    return {
        "message": "Epense Tracker API - test"
    }