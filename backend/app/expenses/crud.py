from datetime import date
from sqlalchemy.orm import Session

from .models import Expense
from .schemas import ExpenseCreate

from app.expenses import enums as expenses_enums


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


def get_expenses(db: Session, 
                 user_id: int | None = None, 
                 category: expenses_enums.ExpenseCategory | None = None, 
                 merchant: str | None = None, 
                 start_date: date | None = None, 
                 end_date: date | None = None, 
                 min_amount: float | None = None, 
                 max_amount: float | None = None, 
                 sort_by: str = "expense_date", 
                 sort_order: str = "desc", 
                 skip: int = 0, 
                 limit: int = 50):
    query = db.query(Expense)

    if user_id is not None:
        query = query.filter(Expense.user_id == user_id)
    if category is not None:
        query = query.filter(Expense.category == category)
    if merchant is not None:
        query = query.filter(Expense.merchant.ilike(f"%{merchant}%"))
    if start_date is not None:
        query = query.filter(Expense.expense_date >= start_date)
    if end_date is not None:
        query = query.filter(Expense.expense_date <= end_date)
    if min_amount is not None:
        query = query.filter(Expense.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Expense.amount <= max_amount)

    sort_columns = {
        "date": Expense.expense_date,
        "amount": Expense.amount,
        "merchant": Expense.merchant,
        "created": Expense.created_at
    }

    column = sort_columns.get(sort_by, Expense.expense_date)

    if sort_order.lower() == "asc":
        query.order_by(column.asc())
    else:
        query.order_by(column.desc())

    return query.offset(skip).limit(limit).all()


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