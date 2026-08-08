from decimal import Decimal
from datetime import date

from pydantic import BaseModel

from app.expenses.enums import ExpenseCategory


class ExpenseAIRequest(BaseModel):
    message: str
    user_id: int


class ExpenseAIResult(BaseModel):
    merchant: str
    description: str
    amount: Decimal
    category: ExpenseCategory
    expense_date: date