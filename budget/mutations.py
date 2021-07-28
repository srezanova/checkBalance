import graphene
from graphql import GraphQLError

from budget.models import Transaction as TransactionModel
from budget.models import Category as CategoryModel
from budget.models import Month as MonthModel
from budget.models import Plan as PlanModel
from .schema import GroupChoice, Transaction, Category, Month, Plan


class CreateTransaction(graphene.Mutation):
    '''Creates transaction'''
    id = graphene.ID()
    amount = graphene.Int()
    description = graphene.String()
    category = graphene.Field(Category)
    month = graphene.Field(Month)
    group = graphene.String()

    class Arguments:
        amount = graphene.Int(required=True)
        group = graphene.String(required=True)
        description = graphene.String(required=True)
        category = graphene.ID()
        month = graphene.ID(required=True)

    @staticmethod
    def mutate(self, info, amount, group, month, category, description=None):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            category_instance = CategoryModel.objects.get(
                id=category, user=user)
        except CategoryModel.DoesNotExist:
            category_instance = None

        try:
            month_instance = MonthModel.objects.get(id=month, user=user)
        except MonthModel.DoesNotExist:
            month_instance = None

        transaction = TransactionModel(
            amount=amount,
            description=description,
            user=user,
            category=category_instance,
            month=month_instance,
            group=group,
        )
        transaction.save()

        return CreateTransaction(id=transaction.id,
                                 amount=amount,
                                 description=description,
                                 category=category_instance,
                                 month=month_instance)


class TransactionInput(graphene.InputObjectType):
    '''
    Arguments for Transaction create/update mutation classes.
    Defines fields allowing user to create or change the data.
    '''
    amount = graphene.Int(required=True)
    description = graphene.String()
    category = graphene.ID(required=True)
    month = graphene.ID(required=True)


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
                category_instance = CategoryModel.objects.get(
                    id=transaction['category'], user=user)
            except CategoryModel.DoesNotExist:
                category_instance = None

            try:
                month_instance = MonthModel.objects.get(
                    id=transaction['month'], user=user)
            except MonthModel.DoesNotExist:
                month_instance = None

            if 'description' not in transaction:
                transaction['description'] = ''

            transaction = TransactionModel.objects.create(
                amount=transaction['amount'],
                description=transaction['description'],
                category=category_instance,
                month=month_instance,
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
    def mutate(self, info, id, amount=None, description=None, category_id=None, month_id=None):

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


class CreateCategory(graphene.Mutation):
    '''
    Creates category. User can't create a category with name that already exists.
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
    '''Updates category. Doesn't update to already existing category.'''
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
    '''Delete category by ID'''

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

        return category


class CreateMonth(graphene.Mutation):
    '''
    Creates month. User can't create month that already exists.
    Default value is 0.
    '''
    id = graphene.ID()
    year = graphene.Int()
    month = graphene.Int()
    start_month_savings = graphene.Int()
    start_month_balance = graphene.Int()

    class Arguments:
        year = graphene.Int(required=True)
        month = graphene.Int(required=True)
        start_month_savings = graphene.Int()
        start_month_balance = graphene.Int()

    @staticmethod
    def mutate(self, info, year, month, start_month_savings=0, start_month_balance=0):

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            month_instance = MonthModel.objects.get(
                year=year, month=month, user=user)
            return CreateMonth(id=month_instance.id,
                               year=year,
                               month=month,
                               start_month_balance=month_instance.start_month_balance,
                               start_month_savings=month_instance.start_month_savings)
        except MonthModel.DoesNotExist:
            month_instance = MonthModel(
                year=year,
                month=month,
                start_month_balance=start_month_balance,
                start_month_savings=start_month_savings,
                user=user
            )
            month_instance.save()
            return CreateMonth(id=month_instance.id,
                               year=year,
                               month=month,
                               start_month_balance=start_month_balance,
                               start_month_savings=start_month_savings)


class UpdateMonth(graphene.Mutation):
    '''Updates category.'''
    id = graphene.ID()
    year = graphene.Int()
    month = graphene.Int()
    start_month_savings = graphene.Int()
    start_month_balance = graphene.Int()

    class Arguments:
        id = graphene.ID(required=True)
        start_month_savings = graphene.Int()
        start_month_balance = graphene.Int()

    @staticmethod
    def mutate(self, info, id, start_month_savings=None, start_month_balance=None):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            month_instance = MonthModel.objects.get(id=id, user=user)
        except MonthModel.DoesNotExist:
            return None

        if start_month_savings is not None:
            month_instance.start_month_savings = start_month_savings
        if start_month_balance is not None:
            month_instance.start_month_balance = start_month_balance
        month_instance.save()
        return UpdateMonth(id=month_instance.id,
                           year=month_instance.year,
                           month=month_instance.month,
                           start_month_savings=month_instance.start_month_savings,
                           start_month_balance=month_instance.start_month_balance)


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
