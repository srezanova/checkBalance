import graphene
from graphene_django import DjangoObjectType, DjangoListField, DjangoConnectionField
from graphql import GraphQLError
import graphene_django_optimizer as gql_optimizer

from .models import Transaction, Category, Month
from users.models import CustomUser

class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser

class TransactionType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = Transaction
        interfaces = (graphene.relay.Node, )

class CategoryType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    class Meta:
        model = Category
        interfaces = (graphene.relay.Node, )

class MonthType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    class Meta:
        model = Month

class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    months = graphene.List(MonthType)
    transactions = graphene.List(TransactionType)

    def resolve_transactions(root, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return gql_optimizer.query(Transaction.objects.filter(user=user), info)

    def resolve_categories(root, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return gql_optimizer.query(Category.objects.filter(user=user), info)

    def resolve_months(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return gql_optimizer.query(Month.objects.filter(user=user), info)

