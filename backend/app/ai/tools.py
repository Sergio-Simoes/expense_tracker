from sqlalchemy.orm import Session
from datetime import date

from app.expenses import crud
from app.expenses import schemas
from app.expenses import enums as expenses_enums

from app.users import crud as users_crud

CATEGORY_VALUES = [category.value for category in expenses_enums.ExpenseCategory]

def create_expense(db: Session, expense: schemas.ExpenseCreate):
    return crud.create_expense(db, expense)


def get_expense(db: Session, expense_id: int):
    return crud.get_expense(db, expense_id)

def get_expenses(db: Session, user_id: int | None = None, category: expenses_enums.ExpenseCategory | None = None, 
                 merchant: str | None = None, start_date: date | None = None, end_date: date | None = None, 
                 min_amount: float | None = None, max_amount: float | None = None, sort_by: str = "expense_date", 
                 sort_order: str = "desc", skip: int = 0, limit: int = 50):
    return crud.get_expenses(db, user_id, category, merchant, start_date, end_date, min_amount, max_amount, sort_by, sort_order, skip, limit)

def update_expense(db: Session, expense_id: int, expense: schemas.ExpenseUpdate):
    return crud.update_expense(db, expense_id, expense)


def delete_expense(db: Session, expense_id: int):
    return crud.delete_expense(db, expense_id)

def get_users(db: Session):
    return users_crud.get_users(db)

create_expense_declaration = {
    "name": "create_expense",
    "description": "Create a new expense in the database.",
    "parameters": {
        "type": "object",
        "properties": {
            "merchant": {
                "type": "string",
                "description": "The merchant or place where the expense happened."
            },
            "description": {
                "type": "string",
                "description": "A short description of the expense."
            },
            "amount": {
                "type": "number",
                "description": "The amount spent."
            },
            "category": {
                "type": "string",
                "enum": CATEGORY_VALUES,
                "description": "The category of the expense."
            }
        },
        "required": [
            "merchant",
            "description",
            "amount",
            "category"
        ]
    }
}

get_expense_declaration = {
    "name": "get_expense",
    "description": "Get a specific expense using its ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "expense_id": {
                "type": "integer",
                "description": "The ID of the expense."
            }
        },
        "required": [
            "expense_id"
        ]
    }
}


get_expenses_declaration = {
    "name": "get_expenses",
    "description": "Retrieve expenses using any combination of filters and sorting options. Only use filters explicitly requested or clearly implied by the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "integer",
                "description": "Filter expenses belonging to a specific user."
            },
            "category": {
                "type": "string",
                "enum": CATEGORY_VALUES,
                "description": "Filter expenses by category."
            },
            "merchant": {
                "type": "string",
                "description": "Filter expenses by merchant, such as Tesco or Amazon."
            },
            "start_date": {
                "type": "string",
                "description": "Return expenses from this date onwards. Format: YYYY-MM-DD."
            },
            "end_date": {
                "type": "string",
                "description": "Return expenses up to this date. Format: YYYY-MM-DD."
            },
            "min_amount": {
                "type": "number",
                "description": "Only return expenses equal to or greater than this amount."
            },
            "max_amount": {
                "type": "number",
                "description": "Only return expenses equal to or less than this amount."
            },
            "sort_by": {
                "type": "string",
                "enum": [
                    "expense_date",
                    "amount",
                    "merchant",
                    "category"
                ],
                "description": "Field to sort the expenses by."
            },
            "sort_order": {
                "type": "string",
                "enum": [
                    "asc",
                    "desc"
                ],
                "description": "Sort direction. Use asc for ascending and desc for descending."
            },
            "skip": {
                "type": "integer",
                "description": "Number of expenses to skip before returning results."
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of expenses to return."
            }
        },
        "required": []
    }
}


update_expense_declaration = {
    "name": "update_expense",
    "description": "Update an existing expense.",
    "parameters": {
        "type": "object",
        "properties": {
            "expense_id": {
                "type": "integer",
                "description": "The ID of the expense to update."
            },
            "merchant": {
                "type": "string",
                "description": "The new merchant."
            },
            "description": {
                "type": "string",
                "description": "The new description."
            },
            "amount": {
                "type": "number",
                "description": "The new amount."
            },
            "category": {
                "type": "string",
                "enum": CATEGORY_VALUES,
                "description": "The new category."
            },
            "expense_date": {
                "type": "string",
                "description": "The new expense date in YYYY-MM-DD format."
            },
            "notes": {
                "type": "string",
                "description": "New notes for the expense."
            }
        },
        "required": [
            "expense_id"
        ]
    }
}


delete_expense_declaration = {
    "name": "delete_expense",
    "description": "Delete an existing expense.",
    "parameters": {
        "type": "object",
        "properties": {
            "expense_id": {
                "type": "integer",
                "description": "The ID of the expense to delete."
            }
        },
        "required": [
            "expense_id"
        ]
    }
}

get_users_declaration = {
    "name": "get_users",
    "description": "Get all users available in the expense tracker. Use this when the user refers to a specific person by name.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}