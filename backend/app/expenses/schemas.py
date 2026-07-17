from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal

from .enums import ExpenseCategory


class ExpenseCreate(BaseModel):

    merchant: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=200)
    amount: Decimal = Field(gt=0)
    category: ExpenseCategory
    expense_date: date
    notes: str | None = Field(default=None, max_length=500)
    user_id: int = Field(gt=0)


class ExpenseResponse(BaseModel):

    id: int
    merchant: str
    description: str | None
    amount: Decimal
    category: ExpenseCategory
    expense_date: date
    created_at: datetime
    notes: str | None
    user_id: int

    class Config:
        from_attributes = True