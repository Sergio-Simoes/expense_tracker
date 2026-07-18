from sqlalchemy.orm import Session

from .models import Expense
from .schemas import ExpenseCreate


def create_expense(db: Session, expense: ExpenseCreate):
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


def get_expenses(db: Session):
    return db.query(Expense).all()


def get_user_expenses(db: Session, user_id: int):
    return (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .all()
    )

def get_expense(db: Session, expense_id: int):
    return (
        db.query(Expense)
        .filter(Expense.id == expense_id)
        .first()
    )

def update_expense(db: Session, expense_id: int, expense_data):
    expense = get_expense(db, expense_id )

    if expense is None:
        return None

    update_data = expense_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "category":
            value = value.value

        setattr(expense, key, value )

    db.commit()
    db.refresh(expense)

    return expense

def delete_expense(db: Session, expense_id: int):
    expense = get_expense(db, expense_id)

    if expense is None:
        return None

    db.delete(expense)
    db.commit()

    return expense