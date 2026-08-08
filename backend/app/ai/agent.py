import os
from datetime import date
from dotenv import load_dotenv
from google import genai
from app.ai.schemas import ExpenseAIResult

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


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