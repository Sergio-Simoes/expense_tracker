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


class TopExpense(BaseModel):
    merchant: str
    amount: Decimal
    category: str


class UserSummary(BaseModel):
    user: str
    total_spent: Decimal
    total_expenses: int
    top_expenses: list[TopExpense]


class HouseholdSummary(BaseModel):
    total_spent: Decimal
    total_expenses: int


class MonthlyReport(BaseModel):
    year: int
    month: int
    household: HouseholdSummary
    categories: list[CategorySummary]
    users: list[UserSummary]