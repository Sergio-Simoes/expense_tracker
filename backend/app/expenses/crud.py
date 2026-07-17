from sqlalchemy.orm import Session

from .models import Expense
from .schemas import ExpenseCreate


def create_expense(
    db: Session,
    expense: ExpenseCreate
):

    db_expense = Expense(
        merchant=expense.merchant,
        description=expense.description,
        amount=expense.amount,
        category=expense.category.value,
        expense_date=expense.expense_date,
        notes=expense.notes,
        user_id=expense.user_id
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense



def get_expenses(
    db: Session
):

    return db.query(Expense).all()



def get_user_expenses(
    db: Session,
    user_id: int
):

    return (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .all()
    )