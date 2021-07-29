import graphene
from graphql import GraphQLError
from graphql_auth.bases import Output

from budget.models import Transaction as TransactionModel
from budget.models import Category as CategoryModel
from budget.models import Month as MonthModel
from budget.schema.transactions import Transaction, TransactionGroups


class CreateTransaction(graphene.Mutation):
    class Arguments:
        amount = graphene.Int(required=True)
        description = graphene.String()
        category = graphene.ID()
        month = graphene.ID(required=True)
        group = TransactionGroups(required=True)

    Output = Transaction

    @staticmethod
    def mutate(self, info, amount, group, month, category=None, description=None):
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
            raise GraphQLError('Month not found.')

        transaction = TransactionModel(
            amount=amount,
            description=description,
            user=user,
            category=category_instance,
            month=month_instance,
            group=group,
        )
        transaction.save()

        return transaction


class TransactionInput(graphene.InputObjectType):
    '''
    Arguments for Transaction create/update mutation classes.
    Defines fields allowing user to create or change the data.
    '''
    amount = graphene.Int(required=True)
    description = graphene.String()
    category = graphene.ID()
    month = graphene.ID(required=True)
    group = TransactionGroups(required=True)


class CreateTransactions(graphene.Mutation):
    '''Creates bulk of transactions'''
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

            if 'category' not in transaction:
                transaction['category'] = None

            try:
                category_instance = CategoryModel.objects.get(
                    id=transaction['category'], user=user)
            except CategoryModel.DoesNotExist:
                category_instance = None

            try:
                month_instance = MonthModel.objects.get(
                    id=transaction['month'], user=user)
            except MonthModel.DoesNotExist:
                continue

            if 'description' not in transaction:
                transaction['description'] = ''

            transaction = TransactionModel.objects.create(
                amount=transaction['amount'],
                description=transaction['description'],
                category=category_instance,
                month=month_instance,
                group=transaction['description'],
                user=user,
            )

            transactions.append(transaction)

        return CreateTransactions(transactions=transactions)


class UpdateTransaction(graphene.Mutation):
    '''Doesn't update category if not found'''

    class Arguments:
        id = graphene.ID(required=True)
        amount = graphene.Int()
        description = graphene.String()
        category = graphene.ID()

    Output = Transaction

    @staticmethod
    def mutate(self, info, id, amount=None, description=None, category=None):

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            transaction = TransactionModel.objects.get(id=id, user=user)
        except TransactionModel.DoesNotExist:
            return None

        if category is not None:
            try:
                category_instance = CategoryModel.objects.get(
                    id=category, user=user)
                transaction.category_id = category
            except CategoryModel.DoesNotExist:
                pass

        if amount is not None:
            transaction.amount = amount
        if description is not None:
            transaction.description = description

        transaction.save()

        return transaction


class DeleteTransaction(graphene.Mutation):
    '''Deletes transaction with given ID'''
    class Arguments:
        id = graphene.ID(required=True)

    Output = Transaction

    @staticmethod
    def mutate(self, info, id):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            transaction = TransactionModel.objects.get(id=id, user=user)
            transaction.delete()
        except TransactionModel.DoesNotExist:
            return None

        return None


class Mutation(graphene.ObjectType):
    create_transaction = CreateTransaction.Field()
    create_transactions = CreateTransactions.Field()
    update_transaction = UpdateTransaction.Field()
    delete_transaction = DeleteTransaction.Field()