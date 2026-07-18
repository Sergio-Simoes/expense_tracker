from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from . import crud, schemas

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/monthly", response_model=schemas.MonthlyReport)
def get_monthly_report(year: int, month: int, db: Session = Depends(get_db)):
    return crud.get_monthly_report(db, year, month)