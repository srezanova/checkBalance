import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
import graphene_django_optimizer as gql_optimizer

from budget.models import Month as MonthModel


class Month(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = MonthModel
        description = "Type definition for a single month."
        exclude = ['user', 'transactions', 'plan']


class Query(graphene.ObjectType):

    month = graphene.Field(Month,
                           id=graphene.ID(required=True),
                           description='Single month query')

    months = graphene.List(Month, description='Months query')

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

    def resolve_months(self, info, id=None, year=None, month=None):
        '''Resolves months'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        return gql_optimizer.query(MonthModel.objects.filter(user=user), info)
