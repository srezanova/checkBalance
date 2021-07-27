import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
import graphene_django_optimizer as gql_optimizer

from users.models import CustomUser as CustomUserModel


class User(DjangoObjectType):
    class Meta:
        model = CustomUserModel
        fields = ['id', 'email']
        description = "Type definition for a single user."


class Query(graphene.ObjectType):
    '''Resolves id and email of authenticated user.'''

    me = graphene.Field(User, description='Current user query')

    def resolve_me(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        return user
