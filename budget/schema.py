import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
import graphene_django_optimizer as gql_optimizer

from .models import Transaction, Category, Month, Plan
from users.models import CustomUser

class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser

class TransactionType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    class Meta:
        model = Transaction

class CategoryType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    class Meta:
        model = Category

class MonthType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    class Meta:
        model = Month

class PlanType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    class Meta:
        model = Plan

class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.ID())
    all_months = graphene.List(MonthType)
    month = graphene.Field(MonthType, id=graphene.ID())
    all_transactions = graphene.List(TransactionType)
    transaction = graphene.Field(TransactionType, id=graphene.ID())
    all_plans = graphene.List(PlanType)
    plan = graphene.Field(PlanType, id=graphene.ID())

    def resolve_all_transactions(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return gql_optimizer.query(Transaction.objects.filter(user=user), info)

    def resolve_transaction(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        transaction = Transaction.objects.get(id=id)
        if transaction.user != user:
            raise GraphQLError('Not found.')
        return transaction

    def resolve_all_categories(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return gql_optimizer.query(Category.objects.filter(user=user), info)

    def resolve_category(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        category = Category.objects.get(id=id)
        if category.user != user:
            raise GraphQLError('Not found.')
        return category

    def resolve__all_months(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return gql_optimizer.query(Month.objects.filter(user=user), info)

    def resolve_month(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        month = Month.objects.get(id=id)
        if month.user != user:
            raise GraphQLError('Not found.')
        return month

    def resolve_all_plans(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return gql_optimizer.query(Plan.objects.filter(user=user), info)

    def resolve_plan(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        plan = Plan.objects.get(id=id)
        if plan.user != user:
            raise GraphQLError('Not found.')
        return plan
