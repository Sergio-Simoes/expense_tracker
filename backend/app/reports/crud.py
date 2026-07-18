from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.expenses.models import Expense

from .schemas import CategorySummary, MonthlyReport


def get_monthly_report(db: Session, year: int, month: int):

    expenses = (
        db.query(Expense)
        .filter(
            extract("year", Expense.expense_date) == year,
            extract("month", Expense.expense_date) == month
        )
    )

    total_spent = expenses.with_entities(func.sum(Expense.amount)).scalar() or 0

    total_expenses = expenses.count()

    category_rows = (
        expenses
        .with_entities(
            Expense.category,
            func.sum(Expense.amount)
        )
        .group_by(Expense.category)
        .all()
    )

    categories = [
        CategorySummary(category=row[0], total=row[1])
        for row in category_rows
    ]

    return MonthlyReport(
        year=year,
        month=month,
        total_spent=total_spent,
        total_expenses=total_expenses,
        categories=categories
    )
