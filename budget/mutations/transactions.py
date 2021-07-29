import graphene
from graphql import GraphQLError

from budget.models import Transaction as TransactionModel
from budget.models import Category as CategoryModel
from budget.models import Month as MonthModel
from budget.schema.transactions import Transaction
from budget.schema.categories import Category
from budget.schema.months import Month


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


class Mutation(graphene.ObjectType):
    create_transaction = CreateTransaction.Field()
    create_transactions = CreateTransactions.Field()
    update_transaction = UpdateTransaction.Field()
    delete_transaction = DeleteTransaction.Field()
