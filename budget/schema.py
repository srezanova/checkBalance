import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
import graphene_django_optimizer as gql_optimizer

from budget.models import Transaction as TransactionModel
from budget.models import Category as CategoryModel
from budget.models import Month as MonthModel
from budget.models import Plan as PlanModel
from users.schema import User


class GroupChoice(graphene.Enum):
    Expense = 'Expense'
    Income = 'Income'
    Savings = 'Savings'


class Transaction(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = TransactionModel
        description = "Type definition for a single transaction."
        exclude = ['user']

    created_at = graphene.String()


class Category(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = CategoryModel
        description = "Type definition for a single category."
        exclude = ['user', 'transactions', 'plan']


class Month(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = MonthModel
        description = "Type definition for a single month."
        exclude = ['user', 'transactions', 'plan']


class Plan(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = PlanModel
        description = "Type definition for a single plan."
        exclude = ['user']


class Query(graphene.ObjectType):
    category = graphene.Field(Category,
                              id=graphene.ID(required=True),
                              description='Single category query')

    categories = graphene.List(Category, description='Categories query')

    month = graphene.Field(Month,
                           id=graphene.ID(required=True),
                           description='Single month query')

    months = graphene.List(Month, description='Months query')

    transaction = graphene.Field(Transaction,
                                 id=graphene.ID(required=True),
                                 description='Single transaction query. Date format YYYY-MM-DD')

    transactions = graphene.List(Transaction,
                                 created_at=graphene.String(),
                                 transaction_description=graphene.String(),
                                 category=graphene.ID(),
                                 month=graphene.ID(),
                                 group=GroupChoice(),
                                 description='Transactions query. Date format YYYY-MM-DD')

    plan = graphene.Field(Plan,
                          id=graphene.ID(required=True),
                          description='Single plan query')

    plans = graphene.List(Plan,
                          category=graphene.ID(),
                          month=graphene.ID(),
                          description='Plans query. Category and month takes ID.')

    def resolve_category(self, info, id):
        '''Resolves single category'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            category = CategoryModel.objects.get(id=id, user=user)
        except CategoryModel.DoesNotExist:
            return None

        return category

    def resolve_transaction(self, info, id):
        '''Resolves single transaction'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            transaction = TransactionModel.objects.get(id=id, user=user)
        except TransactionModel.DoesNotExist:
            return None

        return transaction

    def resolve_month(self, info, id):
        '''Resolves single month'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            month = MonthModel.objects.get(id=id, user=user)
        except MonthModel.DoesNotExist:
            return None

        return month

    def resolve_plan(self, info, id):
        '''Resolves single month'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            plan = PlanModel.objects.get(id=id, user=user)
        except PlanModel.DoesNotExist:
            return None

        return plan

    def resolve_categories(self, info, id=None, name=None, group=None):
        '''Resolves categories'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        return gql_optimizer.query(CategoryModel.objects.filter(user=user), info)

    def resolve_months(self, info, id=None, year=None, month=None):
        '''Resolves months'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        return gql_optimizer.query(MonthModel.objects.filter(user=user), info)

    def resolve_transactions(self,
                             info,
                             group=None,
                             created_at=None,
                             transaction_description=None,
                             category=None,
                             month=None,):
        '''Resolves transactions.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        if category is not None:
            try:
                category_instance = CategoryModel.objects.get(id=category)
            except CategoryModel.DoesNotExist:
                return []

        if month is not None:
            try:
                month_instance = MonthModel.objects.get(id=month)
            except MonthModel.DoesNotExist:
                return []

        # saving passed args for filter and deleting fields we cannot pass in filter
        saved_args = locals()
        del saved_args['self']
        del saved_args['info']
        del saved_args['category']
        del saved_args['month']

        # creating new dict with not None args
        saved_args = {k: v for k, v in saved_args.items() if v is not None}

        return gql_optimizer.query(TransactionModel.objects.filter(**saved_args), info)

    def resolve_plans(self, info, category=None, month=None):
        '''Resolves plans'''

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        category_id = category
        month_id = month

        if category_id is not None:
            try:
                category = CategoryModel.objects.get(id=category_id)
            except CategoryModel.DoesNotExist:
                return []

        if month_id is not None:
            try:
                month = MonthModel.objects.get(id=month_id)
            except MonthModel.DoesNotExist:
                return []

        # saving passed args for filter and deleting fields we cannot pass in filter
        saved_args = locals()

        del saved_args['self']
        del saved_args['info']
        del saved_args['category_id']
        del saved_args['month_id']

        # creating new dict with not None args
        saved_args = {k: v for k, v in saved_args.items() if v is not None}

        return gql_optimizer.query(PlanModel.objects.filter(**saved_args), info)
