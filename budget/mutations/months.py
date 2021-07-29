import graphene
from graphql import GraphQLError

from budget.models import Month as MonthModel
from budget.schema.months import Month


class CreateMonth(graphene.Mutation):
    '''
    Creates month. User can't create month that already exists.
    Month value is a number in range 0, 11.
    Default for start values is 0.
    '''

    class Arguments:
        year = graphene.Int(required=True)
        month = graphene.Int(required=True)
        start_month_savings = graphene.Int()
        start_month_balance = graphene.Int()

    Output = Month

    @staticmethod
    def mutate(self, info, year, month, start_month_savings=0, start_month_balance=0):

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            month_instance = MonthModel.objects.get(
                year=year, month=month, user=user)

        except MonthModel.DoesNotExist:
            month_instance = MonthModel(
                year=year,
                month=month,
                start_month_balance=start_month_balance,
                start_month_savings=start_month_savings,
                user=user
            )

            month_instance.validate_month(month)
            month_instance.save()

        return month_instance


class UpdateMonth(graphene.Mutation):
    '''Updates category's start values with given ID'''
    class Arguments:
        id = graphene.ID(required=True)
        start_month_savings = graphene.Int()
        start_month_balance = graphene.Int()

    Output = Month

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
        return month_instance


class Mutation(graphene.ObjectType):
    create_month = CreateMonth.Field()
    update_month = UpdateMonth.Field()
