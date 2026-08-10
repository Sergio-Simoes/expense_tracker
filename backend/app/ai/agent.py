import os
from datetime import date
from dotenv import load_dotenv
from google import genai
from sqlalchemy.orm import Session

from app.ai.schemas import ExpenseAIResult
from app.ai import tools
from app.expenses import crud as expense_crud
from app.expenses import schemas as expenses_schemas

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def execute_tool(db: Session, function_call, user_id: int):
    name = function_call.name
    arguments = function_call.args

    if name == "create_expense":
        arguments["user_id"] = user_id
        arguments["expense_date"] = arguments.get("expense_date", date.today())
        expense = expenses_schemas.ExpenseCreate(**arguments)
        return tools.create_expense(db, expense)

    if name == "get_expense":
        return tools.get_expense(db, arguments["expense_id"])

    if name == "get_expenses":
        return tools.get_expenses(db, **arguments)

    if name == "update_expense":
        expense_id = arguments.pop("expense_id")
        expense = expenses_schemas.ExpenseUpdate(**arguments)
        return tools.update_expense(db, expense_id, expense)

    if name == "delete_expense":
        return tools.delete_expense(db, arguments["expense_id"])

    return None

def run_agent(db: Session, message: str, user_id: int):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=message,
        config={
            "tools": [
                {
                    "function_declarations": [
                        tools.create_expense_declaration,
                        tools.get_expense_declaration,
                        tools.get_expenses_declaration,
                        tools.update_expense_declaration,
                        tools.delete_expense_declaration
                    ]
                }
            ]
        }
    )

    if not response.function_calls:
        return {"response": response.text}

    function_call = response.function_calls[0]

    return execute_tool(db, function_call, user_id)


def parse_expense(message: str):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
You are an expense extraction assistant.

Extract expense information from the user's message.

Rules:
- amount must be the numerical amount spent
- merchant should be the business or place where the expense happened
- description should briefly describe the expense
- category must be exactly one of: Groceries, Fuel, Restaurants, Pets, Bills, Shopping, Healthcare, Entertainment, Other
- if no date is provided, use today's date
- today's date is {date.today()}

User message:
{message}
""",
        config={
            "response_mime_type": "application/json",
            "response_schema": ExpenseAIResult,
        },
    )

    return ExpenseAIResult.model_validate_json(response.text)


def create_expense_from_message(db:Session, message: str, user_id: int):
    expense_data = parse_expense(message)
    expense_create = expenses_schemas.ExpenseCreate(**expense_data.model_dump(), user_id=user_id)
    return expense_crud.create_expense(db=db, expense=expense_create)