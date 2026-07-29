from datetime import date
from dateutil.relativedelta import relativedelta

from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.expenses.models import Expense
from app.users.models import User

from .schemas import MontthlyTrend, TrendsResponse

from .schemas import (
    CategorySummary,
    HouseholdSummary,
    MonthlyReport,
    TopExpense,
    UserSummary
)

#Helper funcs
def get_month_query(db: Session, year: int, month: int):
    return db.query(Expense).filter(
        extract("year", Expense.expense_date) == year,
        extract("month", Expense.expense_date) == month
    )

def get_total_amount(query):
    return query.with_entities(func.sum(Expense.amount)).scalar or 0

def get_total_expenses(query):
    return query.count()

def get_category_summary(query):
    rows = query.with_entities(
        Expense.category,
        func.sum(Expense.amount)
    ).group_by(
        Expense.category
    ).all()

    return [
        CategorySummary(
            category=row.category,
            total=row[1]
        )
        for row in rows
    ]

def get_top_expenses(query, limit: int = 5):

    expenses = query.order_by(
        Expense.amount.desc()
    ).limit(limit).all()

    return [
        TopExpense(
            merchant=expense.merchant,
            description=expense.description,
            amount=expense.amount,
            category=expense.category,
            expense_date=expense.expense_date
        )
        for expense in expenses
    ]


#Main funcs
def get_monthly_report(db: Session, year: int, month: int):

    monthly_expenses = db.query(Expense).filter(
        extract("year", Expense.expense_date) == year,
        extract("month", Expense.expense_date) == month
    )

    household_total = get_total_amount(monthly_expenses)
    household_count = get_total_expenses(monthly_expenses)

    household = HouseholdSummary(
        total_spent=household_total,
        total_expenses=household_count
    )

    categories = get_category_summary(monthly_expenses)

    users = []

    all_users = db.query(User).all()

    for user in all_users:

        user_expenses = monthly_expenses.filter(
            Expense.user_id == user.id
        )

        total_spent = get_total_amount(user_expenses)
        total_expenses = get_total_expenses(user_expenses)
        top_expenses = get_top_expenses(user_expenses)

        users.append(
            UserSummary(
                user_id=user.id,
                user_name=user.name,
                total_spent=total_spent,
                total_expenses=total_expenses,
                top_expenses=top_expenses
            )
        )

    return MonthlyReport(
        year=year,
        month=month,
        household=household,
        categories=categories,
        users=users
    )

def get_spending_trends(db: Session, months: int):
    today = date.today()
    start = today.replace(day=1) - relativedelta(months=months-1)
    trends = []
    current = start

    while current <= today:
        total = db.query(func.sum(Expense.amount)).filter(
            extract("year", Expense.expense_date) == current.year,
            extract("month", Expense.expense_date) == current.month
        ).scalar() or 0

        trends.append(
            MontthlyTrend(
                year=current.year,
                month=current.month,
                label=current.strftime("%b %Y"),
                total_spent=total
            )
        )

        current += relativedelta(months=1)

    return TrendsResponse(trends=trends)