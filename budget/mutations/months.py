import graphene
from graphql import GraphQLError

from budget.models import Transaction as TransactionModel
from budget.models import Category as CategoryModel
from budget.models import Month as MonthModel
from budget.models import Plan as PlanModel
from budget.schema import GroupChoice, Transaction, Category, Month, Plan


class CreateMonth(graphene.Mutation):
    '''
    Creates month. User can't create month that already exists.
    Default value is 0.
    '''
    id = graphene.ID()
    year = graphene.Int()
    month = graphene.Int()
    start_month_savings = graphene.Int()
    start_month_balance = graphene.Int()

    class Arguments:
        year = graphene.Int(required=True)
        month = graphene.Int(required=True)
        start_month_savings = graphene.Int()
        start_month_balance = graphene.Int()

    @staticmethod
    def mutate(self, info, year, month, start_month_savings=0, start_month_balance=0):

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            month_instance = MonthModel.objects.get(
                year=year, month=month, user=user)
            return CreateMonth(id=month_instance.id,
                               year=year,
                               month=month,
                               start_month_balance=month_instance.start_month_balance,
                               start_month_savings=month_instance.start_month_savings)
        except MonthModel.DoesNotExist:
            month_instance = MonthModel(
                year=year,
                month=month,
                start_month_balance=start_month_balance,
                start_month_savings=start_month_savings,
                user=user
            )
            month_instance.save()
            return CreateMonth(id=month_instance.id,
                               year=year,
                               month=month,
                               start_month_balance=start_month_balance,
                               start_month_savings=start_month_savings)


class UpdateMonth(graphene.Mutation):
    '''Updates category.'''
    id = graphene.ID()
    year = graphene.Int()
    month = graphene.Int()
    start_month_savings = graphene.Int()
    start_month_balance = graphene.Int()

    class Arguments:
        id = graphene.ID(required=True)
        start_month_savings = graphene.Int()
        start_month_balance = graphene.Int()

    @staticmethod
    def mutate(self, info, id, start_month_savings=None, start_month_balance=None):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            month_instance = MonthModel.objects.get(id=id, user=user)
        except MonthModel.DoesNotExist:
            return None

        if start_month_savings is not None:
            month_instance.start_month_savings = start_month_savings
        if start_month_balance is not None:
            month_instance.start_month_balance = start_month_balance
        month_instance.save()
        return UpdateMonth(id=month_instance.id,
                           year=month_instance.year,
                           month=month_instance.month,
                           start_month_savings=month_instance.start_month_savings,
                           start_month_balance=month_instance.start_month_balance)


class Mutation(graphene.ObjectType):
    create_month = CreateMonth.Field()
    update_month = UpdateMonth.Field()
