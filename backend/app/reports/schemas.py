from decimal import Decimal

from pydantic import BaseModel


class CategorySummary(BaseModel):
    category: str
    total: Decimal


class MonthlyReport(BaseModel):
    year: int
    month: int
    total_spent: Decimal
    total_expenses: int
    categories: list[CategorySummary]