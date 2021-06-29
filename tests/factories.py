import factory
from users.models import CustomUser
from factory.django import DjangoModelFactory
from budget.models import Transaction, Category, Month, Plan

class UserFactory(DjangoModelFactory):
    '''
    Define User Factory
    '''
    class Meta:
        model = CustomUser

class CategoryFactory(DjangoModelFactory):
    '''
    Define Offer Factory
    '''
    class Meta:
        model = Category

    # Relationships
    user = factory.SubFactory(UserFactory)
