import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
import graphene_django_optimizer as gql_optimizer

from budget.models import Category as CategoryModel
from budget.models import Month as MonthModel
from budget.models import Plan as PlanModel


class Plan(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = PlanModel
        description = "Type definition for a single plan."
        exclude = ['user']


class Query(graphene.ObjectType):
    plan = graphene.Field(Plan,
                          id=graphene.ID(required=True))

    plans = graphene.List(Plan,
                          category=graphene.ID(),
                          month=graphene.ID())

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
