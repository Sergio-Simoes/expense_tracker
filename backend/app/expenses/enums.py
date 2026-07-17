from enum import Enum


class ExpenseCategory(str, Enum):
    GROCERIES = "Groceries"
    FUEL = "Fuel"
    RESTAURANTS = "Restaurants"
    PETS = "Pets"
    BILLS = "Bills"
    SHOPPING = "Shopping"
    HEALTHCARE = "Healthcare"
    ENTERTAINMENT = "Entertainment"
    OTHER = "Other"