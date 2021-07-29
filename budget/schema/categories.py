import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
import graphene_django_optimizer as gql_optimizer

from budget.models import Category as CategoryModel


class Category(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = CategoryModel
        description = "Type definition for a single category."
        exclude = ['user', 'transactions', 'plan']


class Query(graphene.ObjectType):
    category = graphene.Field(Category,
                              id=graphene.ID(required=True),
                              description='Default color is gray')

    categories = graphene.List(Category)

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

    def resolve_categories(self, info, id=None, name=None, group=None):
        '''Resolves categories'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        return gql_optimizer.query(CategoryModel.objects.filter(user=user), info)
