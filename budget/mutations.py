import graphene
from graphql import GraphQLError

from budget.models import Transaction as TransactionModel
from budget.models import Category as CategoryModel
from budget.models import Month as MonthModel
from budget.models import Plan as PlanModel
from .schema import Transaction, Category, Month, Plan


class TransactionInput(graphene.InputObjectType):
    '''
    Arguments for Transaction create/update mutation classes.
    Defines fields allowing user to create or change the data.
    '''
    transaction_id = graphene.ID()
    amount = graphene.Int()
    description = graphene.String()
    category_id = graphene.ID()
    month_id = graphene.ID()


class CreateTransaction(graphene.Mutation):
    '''Creates a transaction'''
    id = graphene.ID()
    amount = graphene.Int()
    description = graphene.String()
    category = graphene.Field(Category)
    month = graphene.Field(Month)

    class Arguments:
        amount = graphene.Int(required=True)
        description = graphene.String()
        category_id = graphene.ID()
        month_id = graphene.ID()

    @staticmethod
    def mutate(self, info, amount=None, description=None, category_id=None, month_id=None):

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        try:
            category = CategoryModel.objects.get(id=category_id, user=user)
        except CategoryModel.DoesNotExist:
            category = None

        try:
            month = MonthModel.objects.get(id=month_id, user=user)
        except MonthModel.DoesNotExist:
            month = None

        transaction = TransactionModel(
            amount=amount,
            description=description,
            user=user,
            category=category,
            month=month,
        )
        transaction.save()

        return CreateTransaction(id=transaction.id,
                                 amount=amount,
                                 description=description,
                                 category=category,
                                 month=month)


class CreateManyTransactions(graphene.Mutation):
    class Input:
        transactions = graphene.List(TransactionInput)

    transactions = graphene.List(lambda: Transaction)

    @ staticmethod
    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        transactions = []
        for transaction in kwargs.get('transactions'):
            if transaction.category_id is not None:
                category = CategoryModel.objects.get(
                    id=transaction.category_id)
                if category.user != user:
                    raise GraphQLError(
                        "Can't find category with given category ID.")
            if transaction.month_id is not None:
                month = MonthModel.objects.get(
                    id=transaction.month_id, user=user)
                if month.user != user:
                    raise GraphQLError("Can't find month with given month ID.")
            transaction = TransactionModel.objects.create(
                amount=transaction.amount,
                description=transaction.description,
                category_id=transaction.category_id,
                month_id=transaction.month_id,
                user=user,
            )
            transactions.append(transaction)
        return CreateManyTransactions(transactions=transactions)


class UpdateTransaction(graphene.Mutation):
    transaction = graphene.Field(Transaction)

    class Arguments:
        transaction_data = TransactionInput(required=True)

    @staticmethod
    def mutate(self, info, transaction_data=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        transaction = TransactionModel.objects.get(
            pk=transaction_data.transaction_id)
        if transaction.user != user:
            raise GraphQLError('Not permitted to update this transaction.')
        if transaction_data.amount is not None:
            transaction.amount = transaction_data.amount
        if transaction_data.description is not None:
            transaction.description = transaction_data.description
        if transaction_data.category_id is not None:
            category = CategoryModel.objects.get(
                id=transaction_data.category_id)
            if category.user != user:
                raise GraphQLError(
                    "Can't find category with given category ID.")
            transaction.category_id = transaction_data.category_id
        if transaction_data.month_id is not None:
            month = MonthModel.objects.get(id=transaction_data.month_id)
            if month.user != user:
                raise GraphQLError("Can't find month with given month ID.")
            transaction.month_id = transaction_data.month_id

        transaction.save()
        return UpdateTransaction(transaction=transaction)


class DeleteTransaction(graphene.Mutation):
    transaction = graphene.Field(Transaction)

    class Arguments:
        transaction_id = graphene.ID(required=True)

    @staticmethod
    def mutate(self, info, transaction_id):
        user = info.context.user
        transaction_instance = TransactionModel.objects.get(id=transaction_id)
        if transaction_instance.user != user:
            raise GraphQLError('Not permitted to delete this transaction.')
        transaction_instance.delete()
        return None


class CategoryInput(graphene.InputObjectType):
    '''
    Arguments for Category create/update mutation classes.
    Defines fields allowing user to create or change caregory data.
    '''
    category_id = graphene.ID()
    name = graphene.String()
    group = graphene.String()


class CreateCategory(graphene.Mutation):
    '''
    User can't create a category with name that already exists.
    '''
    category = graphene.Field(Category)

    class Arguments:
        category_data = CategoryInput(required=True)

    @staticmethod
    def mutate(self, info, category_data):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        if CategoryModel.objects.filter(
            name=category_data.name,
            group=category_data.group,
            user=user
        ).exists():
            raise GraphQLError('Category with this name already exists.')
        category_instance = CategoryModel(
            name=category_data.name,
            group=category_data.group,
            user=user,
        )
        category_instance.save()
        return CreateCategory(category=category_instance)


class UpdateCategory(graphene.Mutation):
    category = graphene.Field(Category)

    class Arguments:
        category_data = CategoryInput(required=True)

    @staticmethod
    def mutate(self, info, category_data=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        category_instance = CategoryModel.objects.get(
            id=category_data.category_id,
        )
        if category_instance.user != user:
            raise GraphQLError('Not permitted to update this category')
        if CategoryModel.objects.filter(
            name=category_data.name,
            group=category_instance.group,
            user=user
        ).exists():
            raise GraphQLError('Category with this name already exists.')
        if CategoryModel.objects.filter(
            name=category_instance.name,
            group=category_data.group,
            user=user
        ).exists():
            raise GraphQLError('Category with this name already exists.')
        if category_data.name is not None:
            category_instance.name = category_data.name
        if category_data.group is not None:
            category_instance.group = category_data.group
        category_instance.save()
        return UpdateCategory(category=category_instance)


class DeleteCategory(graphene.Mutation):
    category = graphene.Field(Category)

    class Arguments:
        category_id = graphene.ID(required=True)

    def mutate(self, info, category_id):
        user = info.context.user
        category_instance = CategoryModel.objects.get(id=category_id)
        if category_instance.user != user:
            raise GraphQLError("Not permitted to delete this category")
        category_instance.delete()
        return None


class MonthInput(graphene.InputObjectType):
    '''
    Arguments for Month create/update mutation classes.
    Defines fields allowing user to create or change the month data.
    '''
    month_id = graphene.ID()
    year = graphene.String()
    month = graphene.String()
    start_month_savings = graphene.Int()
    start_month_balance = graphene.Int()


class CreateMonth(graphene.Mutation):
    month = graphene.Field(Month)

    class Arguments:
        month_data = MonthInput(required=True)

    @staticmethod
    def mutate(self, info, month_data):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        if MonthModel.objects.filter(
            month=month_data.month,
            year=month_data.year,
            user=user
        ).exists():
            raise GraphQLError('Created month already exists.')
        month_instance = MonthModel(
            year=month_data.year,
            month=month_data.month,
            start_month_balance=month_data.start_month_balance,
            start_month_savings=month_data.start_month_savings,
            user=user)
        month_instance.save()
        return CreateMonth(month=month_instance)


class UpdateMonth(graphene.Mutation):
    month = graphene.Field(Month)

    class Arguments:
        month_data = MonthInput(required=True)

    @staticmethod
    def mutate(self, info, month_data=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        month_instance = MonthModel.objects.get(id=month_data.month_id)
        if month_instance.user != user:
            raise GraphQLError('Not permitted to update this month.')
        if month_data.year is not None:
            month_instance.year = month_data.year
        if month_data.month is not None:
            month_instance.month = month_data.month
        if month_data.start_month_savings is not None:
            month_instance.start_month_savings = month_data.start_month_savings
        if month_data.start_month_balance is not None:
            month_instance.start_month_balance = month_data.start_month_balance
        month_instance.save()
        return UpdateMonth(month=month_instance)


class PlanInput(graphene.InputObjectType):
    '''
    Arguments for Month create/update mutation classes.
    Defines fields allowing user to create or change plan data.
    User can create plan after creating caregory and month.
    User can create only one plan within month.
    '''
    plan_id = graphene.ID()
    month_id = graphene.ID(required=True)
    category_id = graphene.ID(required=True)
    planned_amount = graphene.Int(required=True)


class CreatePlan(graphene.Mutation):
    plan = graphene.Field(Plan)

    class Arguments:
        plan_data = PlanInput(required=True)

    @staticmethod
    def mutate(self, info, plan_data):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        category = CategoryModel.objects.get(id=plan_data.category_id)
        if category.user != user:
            raise GraphQLError("Can't find category with given category ID.")
        month = MonthModel.objects.get(id=plan_data.month_id, user=user)
        if not month:
            raise GraphQLError("Can't find month with given month ID.")
        if PlanModel.objects.filter(
            category_id=plan_data.category_id,
            month_id=plan_data.month_id,
            user=user
        ).exists():
            raise GraphQLError('Created plan already exists.')

        plan_instance = PlanModel(
            planned_amount=plan_data.planned_amount,
            user=user,
            category_id=plan_data.category_id,
            month_id=plan_data.month_id,
        )
        plan_instance.save()
        return CreatePlan(plan=plan_instance)


class UpdatePlan(graphene.Mutation):
    plan = graphene.Field(Plan)

    class Arguments:
        plan_id = graphene.ID(required=True)
        planned_amount = graphene.Int(required=True)

    @staticmethod
    def mutate(self, info, plan_id, planned_amount):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        plan = PlanModel.objects.get(id=plan_id)
        if plan.user != user:
            raise GraphQLError('Not permitted to update this plan.')
        plan.planned_amount = planned_amount
        plan.save()
        return UpdatePlan(plan=plan)


class Mutation(graphene.ObjectType):
    create_transaction = CreateTransaction.Field()
    create_many_transactions = CreateManyTransactions.Field()
    update_transaction = UpdateTransaction.Field()
    delete_transaction = DeleteTransaction.Field()
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
    create_month = CreateMonth.Field()
    update_month = UpdateMonth.Field()
    create_plan = CreatePlan.Field()
    update_plan = UpdatePlan.Field()
