import graphene
from graphql import GraphQLError

from .models import Transaction, Category, Month
from .schema import UserType, TransactionType, CategoryType, MonthType



class TransactionInput(graphene.InputObjectType):
    '''
    Arguments for Transaction create/update mutation classes.
    Defines fields allowing user to create or change the data.
    '''
    transaction_id = graphene.ID()
    amount = graphene.Int()
    description = graphene.String()
    category_id = graphene.Int()
    month_id = graphene.Int()

class CreateTransaction(graphene.Mutation):
    '''
    Creates a transaction.

    Takes arguments: amount, description, category_id, month_id.

    User can access only personal categories/months.
    '''
    transaction = graphene.Field(TransactionType)

    class Arguments:
        transaction_data = TransactionInput(required=True)

    @staticmethod
    def mutate(root, info, transaction_data):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        category = Category.objects.get(
            id=transaction_data.category_id,
            user=user)
        if not category:
            raise GraphQLError("Can't find category with given category_id.")
        month = Month.objects.get(id=transaction_data.month_id, user=user)
        if not month:
            raise GraphQLError("Can't find month with given month_id.")
        transaction_instance = Transaction(
            amount=transaction_data.amount,
            description=transaction_data.description,
            user=user,
            category=category,
            month=month,
            )
        transaction_instance.save()
        return CreateTransaction(transaction=transaction_instance)

class CreateManyTransactions(graphene.Mutation):
    '''
    Creates bulk of transactions.

    Takes arguments: amount, description, category_id, month_id.

    User can access only personal categories/months.
    '''
    class Input:
       transactions = graphene.List(TransactionInput)

    transactions = graphene.List(lambda: TransactionType)

    @staticmethod
    def mutate(root, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')

        transactions = [Transaction.objects.create(
            amount=transaction.amount,
            description=transaction.description,
            category_id=transaction.category_id,
            month_id=transaction.month_id,
            user=user,
            ) for transaction in kwargs.get('transactions')]
        return CreateManyTransactions(transactions=transactions)

class UpdateTransaction(graphene.Mutation):
    '''
    Updates transaction data.

    Takes arguments: transaction_id and data user wants to change.
    All optional: amount, description, category_id, month_id.

    User can update only personal transactions with personal categories.
    '''
    transaction = graphene.Field(TransactionType)

    class Arguments:
        transaction_data = TransactionInput(required=True)

    @staticmethod
    def mutate(root, info, transaction_data=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        transaction = Transaction.objects.get(pk=transaction_data.transaction_id)
        if transaction.user != user:
            raise GraphQLError('Not permitted to update this transaction.')
        if transaction_data.amount is not None:
            transaction.amount = transaction_data.amount
        if transaction_data.description is not None:
            transaction.description = transaction_data.description
        if transaction_data.category_id is not None:
            category = Category.objects.get(id=transaction_data.category_id)
            if category.user != user:
                raise GraphQLError("Can't find category with given category_id.")
            transaction.category_id = transaction_data.category_id
        if transaction_data.month_id is not None:
            month = Month.objects.get(id=transaction_data.month_id)
            if month.user != user:
                raise GraphQLError("Can't find month with given month_id.")
            transaction.month_id = transaction_data.month_id

        transaction.save()
        return UpdateTransaction(transaction=transaction)

class DeleteTransaction(graphene.Mutation):
    '''
    Deletes transactions.

    Takes argument: transaction_id - required!
    '''
    transaction =  graphene.Field(TransactionType)

    class Arguments:
        transaction_id = graphene.Int(required=True)

    def mutate(root, info, transaction_id):
        user = info.context.user
        transaction_instance = Transaction.objects.get(id=transaction_id)
        if transaction_instance.user != user:
            raise GraphQLError('Not permitted to delete this transaction.')
        transaction_instance.delete()
        return None

class CategoryInput(graphene.InputObjectType):
    '''
    Arguments for Category create/update mutation classes.
    Defines fields allowing user to create or change the data.
    '''
    category_id = graphene.ID()
    name = graphene.String()
    group = graphene.String()

class CreateCategory(graphene.Mutation):
    '''
    Creates a category.

    Takes arguments: amount, description, category_id.

    User can access only personal categories.
    '''
    category = graphene.Field(CategoryType)

    class Arguments:
        category_data = CategoryInput(required=True)

    @staticmethod
    def mutate(root, info, category_data):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        category_instance = Category(
            name = category_data.name,
            group = category_data.group,
            user = user,
        )
        category_instance.save()
        return CreateCategory(category=category_instance)

class UpdateCategory(graphene.Mutation):
    '''
    Updates category data.

    Takes arguments: category_id and data user wants to change.
    All optional: name, group.

    User can update only personal categories.
    '''
    category = graphene.Field(CategoryType)

    class Arguments:
        category_data = CategoryInput(required=True)

    @staticmethod
    def mutate(root, info, category_data=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        category_instance = Category.objects.get(
            id=category_data.category_id,
            )
        if category_instance.user != user:
            raise GraphQLError('Not permitted to update this category')
        if category_data.name is not None:
            category_instance.name = category_data.name
        if category_data.group is not None:
            category_instance.group = category_data.group
        category_instance.save()
        return UpdateCategory(category=category_instance)

class DeleteCategory(graphene.Mutation):
    '''
    Deletes categories.

    Takes argument: category_id - required!
    '''
    category = graphene.Field(CategoryType)

    class Arguments:
        category_id = graphene.Int(required=True)

    def mutate(root, info, category_id):
        user = info.context.user
        category_instance = Category.objects.get(id=category_id)
        if category_instance.user != user:
            raise GraphQLError("Not permitted to delete this category")
        category_instance.delete()
        return None

class MonthInput(graphene.InputObjectType):
    '''
    Arguments for Month create/update mutation classes.
    Defines fields allowing user to create or change the data.
    '''
    month_id = graphene.ID()
    year = graphene.String()
    month = graphene.String()
    start_month_savings = graphene.Int()
    start_month_balance = graphene.Int()

class CreateMonth(graphene.Mutation):
    '''
    Creates month.

    Takes arguments: year, month, start_month_savings, start_month_balance.
    '''
    month = graphene.Field(MonthType)

    class Arguments:
        month_data = MonthInput(required=True)

    @staticmethod
    def mutate(root, info, month_data):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        month_instance = Month(
            year=month_data.year,
            month=month_data.month,
            start_month_balance=month_data.start_month_balance,
            start_month_savings=month_data.start_month_savings,
            user=user)
        month_instance.save()
        return CreateMonth(month=month_instance)

class UpdateMonth(graphene.Mutation):
    '''
    Updates month data.

    Takes arguments: month_id and data user wants to change.

    All optional: year, month, start_month_savings, start_month_balance.
    '''
    month = graphene.Field(MonthType)

    class Arguments:
        month_data = MonthInput(required=True)

    @staticmethod
    def mutate(root, info, month_data=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        month_instance = Month.objects.get(id=month_data.month_id)
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