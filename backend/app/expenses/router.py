from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.expenses import crud as expense_crud
from app.expenses import schemas as expense_schemas
from app.expenses import enums as expenses_enums

from . import schemas, crud


router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=schemas.ExpenseResponse)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense( db, expense )


@router.get("/", response_model=list[schemas.ExpenseResponse])
def get_expenses(db: Session = Depends(get_db), user_id: int | None = None, category: expenses_enums.ExpenseCategory | None = None, 
                 merchant: str | None = None, start_date: date | None = None, end_date: date | None = None, 
                 min_amount: float | None = None, max_amount: float | None = None):
    return crud.get_expenses(db, user_id, category, merchant, start_date, end_date, min_amount, max_amount)


@router.get("/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = crud.get_expense(db, expense_id)

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense


@router.put( "/{expense_id}", response_model=schemas.ExpenseResponse )
def update_expense(expense_id: int, expense: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    updated = crud.update_expense(db, expense_id, expense)

    if updated is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    return updated


@router.delete( "/{expense_id}" )
def delete_expense( expense_id: int, db: Session = Depends(get_db) ):
    deleted = crud.delete_expense( db, expense_id )

    if deleted is None:
        raise HTTPException( status_code=404, detail="Expense not found" )

    return {"message": "Expense deleted successfully"}


@router.get("/{user_id}/expenses", response_model=list[expense_schemas.ExpenseResponse])
def get_user_expenses(user_id: int, db: Session = Depends(get_db)):
    return expense_crud.get_user_expenses(db, user_id)