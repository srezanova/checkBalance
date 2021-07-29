import graphene
from graphql import GraphQLError

from budget.models import Transaction as TransactionModel
from budget.models import Category as CategoryModel
from budget.models import Month as MonthModel
from budget.models import Plan as PlanModel
from budget.schema import GroupChoice, Transaction, Category, Month, Plan


class CreatePlan(graphene.Mutation):
    '''Creates plan.'''
    id = graphene.ID()
    category = graphene.Field(Category)
    month = graphene.Field(Month)
    planned_amount = graphene.Int()

    class Arguments:
        category_id = graphene.ID(required=True)
        month_id = graphene.ID(required=True)
        planned_amount = graphene.Int(required=True)

    @staticmethod
    def mutate(self, info, category_id, month_id, planned_amount):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            category = CategoryModel.objects.get(id=category_id, user=user)
        except CategoryModel.DoesNotExist:
            raise GraphQLError('Category not found.')

        try:
            month = MonthModel.objects.get(id=month_id, user=user)
        except MonthModel.DoesNotExist:
            raise GraphQLError('Month not found.')

        plan = PlanModel(
            planned_amount=planned_amount,
            user=user,
            category=category,
            month=month,
        )
        plan.save()

        return CreatePlan(id=plan.id,
                          planned_amount=planned_amount,
                          category=category,
                          month=month)


class UpdatePlan(graphene.Mutation):
    '''Updates planned amount.'''
    id = graphene.ID()
    category = graphene.Field(Category)
    month = graphene.Field(Month)
    planned_amount = graphene.Int()

    class Arguments:
        id = graphene.ID(required=True)
        planned_amount = graphene.Int(required=True)

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
        return UpdatePlan(id=plan.id,
                          planned_amount=plan.planned_amount,
                          month=plan.month,
                          category=plan.category)


class Mutation(graphene.ObjectType):
    create_plan = CreatePlan.Field()
    update_plan = UpdatePlan.Field()
