from fastapi import APIRouter

from . import schemas, agent

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/parse-expense", response_model=schemas.ExpenseAIResult)
def parse_expense(request: schemas.ExpenseAIRequest):
    return agent.parse_expense(request.message)