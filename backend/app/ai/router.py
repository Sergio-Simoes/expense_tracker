from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from . import schemas, agent

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/parse-expense", response_model=schemas.ExpenseAIResult)
def parse_expense(request: schemas.ExpenseAIRequest):
    return agent.parse_expense(request.message)


@router.post("/create-expense")
def create_expense(request: schemas.ExpenseAIRequest, db: Session = Depends(get_db)):
    return agent.create_expense_from_message(db, request.message, request.user_id)

@router.post("/agent")
def run_agent(request: schemas.ExpenseAIRequest, db: Session = Depends(get_db)):
    return agent.run_agent(db, request.message, request.user_id)