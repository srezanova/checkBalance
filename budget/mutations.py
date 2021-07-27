import graphene
from graphql import GraphQLError

from budget.models import Transaction as TransactionModel
from budget.models import Category as CategoryModel
from budget.models import Month as MonthModel
from budget.models import Plan as PlanModel
from .schema import GroupChoice, YearChoice, MonthChoice, Transaction, Category, Month, Plan


class CreateTransaction(graphene.Mutation):
    '''Creates transaction'''
    id = graphene.ID()
    amount = graphene.Int()
    description = graphene.String()
    category = graphene.Field(Category)
    month = graphene.Field(Month)

    class Arguments:
        amount = graphene.Int(required=True)
        description = graphene.String()
        category_id = graphene.ID()
        month_id = graphene.ID(required=True)

    @staticmethod
    def mutate(self, info, amount=None, description=None, category_id=None, month_id=None):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

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


class TransactionInput(graphene.InputObjectType):
    '''
    Arguments for Transaction create/update mutation classes.
    Defines fields allowing user to create or change the data.
    '''
    amount = graphene.Int(required=True)
    description = graphene.String()
    category_id = graphene.ID()
    month_id = graphene.ID(required=True)


class CreateTransactions(graphene.Mutation):
    '''Creates bulk of transactions.'''
    transactions = graphene.List(lambda: Transaction)

    class Input:
        transactions = graphene.List(TransactionInput)

    @ staticmethod
    def mutate(self, info, **kwargs):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        transactions = []

        for transaction in kwargs.get('transactions'):

            try:
                category = CategoryModel.objects.get(
                    id=transaction['category_id'], user=user)
            except CategoryModel.DoesNotExist:
                category = None

            try:
                month = MonthModel.objects.get(
                    id=transaction['month_id'], user=user)
            except MonthModel.DoesNotExist:
                month = None

            transaction = TransactionModel.objects.create(
                amount=transaction['amount'],
                description=transaction['description'],
                category=category,
                month=month,
                user=user,
            )

            transactions.append(transaction)

        return CreateTransactions(transactions=transactions)


class UpdateTransaction(graphene.Mutation):
    '''Updates transaction.
    If updated category / month not found they stay the same.'''
    id = graphene.ID()
    amount = graphene.Int()
    description = graphene.String()
    category = graphene.Field(Category)
    month = graphene.Field(Month)

    class Arguments:
        id = graphene.ID(required=True)
        amount = graphene.Int()
        description = graphene.String()
        category_id = graphene.ID()
        month_id = graphene.ID()

    @staticmethod
    def mutate(self, info, id=None, amount=None, description=None, category_id=None, month_id=None):

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            transaction = TransactionModel.objects.get(id=id, user=user)
        except TransactionModel.DoesNotExist:
            return None

        try:
            category = CategoryModel.objects.get(id=category_id, user=user)
            transaction.category_id = category_id
        except CategoryModel.DoesNotExist:
            category_id = transaction.category_id
            category = CategoryModel.objects.get(id=category_id, user=user)
            transaction.category_id = category_id

        try:
            month = MonthModel.objects.get(id=month_id, user=user)
            transaction.month_id = month_id
        except MonthModel.DoesNotExist:
            month_id = transaction.month_id
            month = MonthModel.objects.get(id=month_id, user=user)
            transaction.month_id = month_id

        if amount is not None:
            transaction.amount = amount
        if description is not None:
            transaction.description = description

        transaction.save()

        return UpdateTransaction(id=transaction.id,
                                 amount=transaction.amount,
                                 description=transaction.description,
                                 category=category,
                                 month=month)


class DeleteTransaction(graphene.Mutation):
    '''Deletes transaction. Returns boolean.'''
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    @staticmethod
    def mutate(self, info, id):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            transaction = TransactionModel.objects.get(id=id, user=user)
            transaction.delete()
            success = True
        except TransactionModel.DoesNotExist:
            success = False

        return DeleteTransaction(success=success)


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
    Creates category. User can't create a category with name that already exists.
    '''
    id = graphene.ID()
    name = graphene.String()
    group = GroupChoice()

    class Arguments:
        name = graphene.String(required=True)
        group = GroupChoice(required=True)

    @staticmethod
    def mutate(self, info, name, group):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            category = CategoryModel.objects.get(name=name,
                                                 group=group,
                                                 user=user)
            return CreateCategory(id=category.id,
                                  name=name,
                                  group=group)

        except CategoryModel.DoesNotExist:
            category = CategoryModel(
                name=name,
                group=group,
                user=user,
            )
            category.save()
            return CreateCategory(id=category.id,
                                  name=name,
                                  group=group)


class UpdateCategory(graphene.Mutation):
    category = graphene.Field(Category)

    class Arguments:
        category_data = CategoryInput(required=True)

    @staticmethod
    def mutate(self, info, category_data=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')
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
            raise GraphQLError('Unauthorized.')
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
            raise GraphQLError('Unauthorized.')
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
            raise GraphQLError('Unauthorized.')
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
            raise GraphQLError('Unauthorized.')
        plan = PlanModel.objects.get(id=plan_id)
        if plan.user != user:
            raise GraphQLError('Not permitted to update this plan.')
        plan.planned_amount = planned_amount
        plan.save()
        return UpdatePlan(plan=plan)


class Mutation(graphene.ObjectType):
    create_transaction = CreateTransaction.Field()
    create_transactions = CreateTransactions.Field()
    update_transaction = UpdateTransaction.Field()
    delete_transaction = DeleteTransaction.Field()
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
    create_month = CreateMonth.Field()
    update_month = UpdateMonth.Field()
    create_plan = CreatePlan.Field()
    update_plan = UpdatePlan.Field()
