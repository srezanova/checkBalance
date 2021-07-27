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


class YearChoice(graphene.Enum):
    A_2021 = '2021'
    A_2022 = '2022'
    A_2023 = '2023'


class MonthChoice(graphene.Enum):
    January = 'January'
    February = 'February'
    March = 'March'
    April = 'April'
    May = 'May'
    June = 'June'
    July = 'July'
    August = 'August'
    September = 'September'
    October = 'October'
    November = 'November'
    December = 'December'


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
    categories = graphene.List(Category,
                               id=graphene.ID(),
                               name=graphene.String(),
                               group=GroupChoice(),
                               description='Categories query')

    months = graphene.List(Month,
                           id=graphene.ID(),
                           year=YearChoice(),
                           month=MonthChoice(),
                           description='Months query')

    transactions = graphene.List(Transaction,
                                 id=graphene.ID(),
                                 created_at=graphene.String(),
                                 amount=graphene.Int(),
                                 desc=graphene.String(),
                                 category_id=graphene.ID(),
                                 month_id=graphene.ID(),
                                 description='Transactions query')

    plans = graphene.List(Plan,
                          id=graphene.ID(),
                          category_id=graphene.ID(),
                          month_id=graphene.ID(),
                          description='Plans query')

    def resolve_categories(self, info, id=None, name=None, group=None):
        '''Resolves categories'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        # saving passed args for filter and deleting fields we cannot pass in filter
        saved_args = locals()
        del saved_args['self']
        del saved_args['info']

        # creating new dict with not None args
        saved_args = {k: v for k, v in saved_args.items() if v is not None}

        return gql_optimizer.query(CategoryModel.objects.filter(**saved_args), info)

    def resolve_months(self, info, id=None, year=None, month=None):
        '''Resolves months'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        # saving passed args for filter and deleting fields we cannot pass in filter
        saved_args = locals()
        del saved_args['self']
        del saved_args['info']

        # creating new dict with not None args
        saved_args = {k: v for k, v in saved_args.items() if v is not None}

        return gql_optimizer.query(MonthModel.objects.filter(**saved_args), info)

    def resolve_transactions(self,
                             info,
                             id=None,
                             created_at=None,
                             amount=None,
                             desc=None,
                             category_id=None,
                             month_id=None,):
        '''Resolves transactions.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

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

        return gql_optimizer.query(TransactionModel.objects.filter(**saved_args), info)

    def resolve_plans(self, info, id=None, category_id=None, month_id=None):
        '''Resolves plans'''

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

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
