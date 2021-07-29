import graphene
from graphql import GraphQLError

from budget.models import Category as CategoryModel
from budget.schema.categories import Category


class CreateCategory(graphene.Mutation):
    '''
    User can't create a category with name that already exists.
    Default color is gray
    '''
    class Arguments:
        name = graphene.String(required=True)
        color = graphene.String()

    Output = Category

    @staticmethod
    def mutate(self, info, name, color='gray'):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            category = CategoryModel.objects.get(name=name,
                                                 user=user)

        except CategoryModel.DoesNotExist:
            category = CategoryModel(
                name=name,
                color=color,
                user=user,
            )
            category.save()
            return category


class UpdateCategory(graphene.Mutation):
    '''Doesn't update to already existing category'''
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        color = graphene.String()

    Output = Category

    @staticmethod
    def mutate(self, info, id, name=None, color=None):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            category = CategoryModel.objects.get(id=id, user=user)
        except CategoryModel.DoesNotExist:
            return None

        try:
            category = CategoryModel.objects.get(name=name,
                                                 user=user)
        except CategoryModel.DoesNotExist:
            if name is not None:
                category.name = name

        if color is not None:
            category.color = color

        category.save()

        return category


class DeleteCategory(graphene.Mutation):
    '''Delete category with given ID'''

    class Arguments:
        id = graphene.ID(required=True)

    Output = Category

    def mutate(self, info, id):

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            category = CategoryModel.objects.get(id=id, user=user)
            category.delete()
        except CategoryModel.DoesNotExist:
            return None

        return None


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
