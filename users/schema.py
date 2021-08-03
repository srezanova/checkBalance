import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
import graphene_django_optimizer as gql_optimizer

from .models import CustomUser


class User(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'avatar']
        description = "Type definition for a single user"


class Query(graphene.ObjectType):
    '''Resolves id and email of authenticated user.'''

    me = graphene.Field(User, description='Current user query')

    def resolve_me(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        user.avatar = user.gravatar_url()

        return user
