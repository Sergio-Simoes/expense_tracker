from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from . import schemas, crud


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"]
)


@router.post(
    "/",
    response_model=schemas.ExpenseResponse
)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db)
):

    return crud.create_expense(
        db,
        expense
    )


@router.get(
    "/",
    response_model=list[schemas.ExpenseResponse]
)
def get_expenses(
    db: Session = Depends(get_db)
):

    return crud.get_expenses(db)