import graphene
from graphql import GraphQLError
from graphql_auth.bases import Output

from budget.models import Transaction as TransactionModel
from budget.models import Category as CategoryModel
from budget.models import Month as MonthModel
from budget.models import Plan as PlanModel
from budget.schema import GroupChoice, Transaction, Category, Month, Plan


class CreatePlan(graphene.Mutation):
    '''Creates plan'''
    class Arguments:
        category = graphene.ID(required=True)
        month = graphene.ID(required=True)
        planned_amount = graphene.Int(required=True)

    Output = Plan

    @staticmethod
    def mutate(self, info, category, month, planned_amount):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            category_instance = CategoryModel.objects.get(
                id=category, user=user)
        except CategoryModel.DoesNotExist:
            raise GraphQLError('Category not found.')

        try:
            month_instance = MonthModel.objects.get(id=month, user=user)
        except MonthModel.DoesNotExist:
            raise GraphQLError('Month not found.')

        plan = PlanModel(
            planned_amount=planned_amount,
            user=user,
            category=category_instance,
            month=month_instance,
        )
        plan.save()

        return plan


class UpdatePlan(graphene.Mutation):
    '''Updates planned amount with given ID'''
    class Arguments:
        id = graphene.ID(required=True)
        planned_amount = graphene.Int(required=True)

    Output = Plan

    @staticmethod
    def mutate(self, info, id, planned_amount):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            plan = PlanModel.objects.get(id=id, user=user)
        except PlanModel.DoesNotExist:
            return None

        plan.planned_amount = planned_amount
        plan.save()
        return plan


class Mutation(graphene.ObjectType):
    create_plan = CreatePlan.Field()
    update_plan = UpdatePlan.Field()
