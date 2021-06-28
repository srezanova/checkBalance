from users.models import CustomUser
from budget.models import Transaction, Month, Transaction, Category, Plan

def initialize():
    user = CustomUser(email="test@example.com", password="testpassword")
    user.save()

    category = Category(name="Netflix", group="Expense")
    category.save()