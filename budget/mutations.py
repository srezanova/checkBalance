import graphene
from graphql import GraphQLError

from .models import Transaction, Category, Month
from .schema import UserType, TransactionType, CategoryType, MonthType



class TransactionInput(graphene.InputObjectType):
    '''
    Argument for our mutation classes.
    Defines fields allowing user to add or change the data.
    '''
    transaction_id = graphene.ID()
    amount = graphene.Int()
    description = graphene.String()
    category_id = graphene.Int()

class CreateTransaction(graphene.Mutation):
    '''
    Create a transaction.

    Takes arguments: amount, description, category_id.

    User can access only personal categories.
    '''
    transaction = graphene.Field(TransactionType)

    class Arguments:
        transaction_data = TransactionInput(required=True)

    @staticmethod
    def mutate(root, info, transaction_data):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        category = Category.objects.get(id=transaction_data.category_id, user=user)
        if not category:
            raise GraphQLError("Can't find category with given category id.")
        transaction_instance = Transaction(
            amount=transaction_data.amount,
            description=transaction_data.description,
            user=user,
            category=category,
            )
        transaction_instance.save()
        return CreateTransaction(transaction=transaction_instance)

class UpdateTransaction(graphene.Mutation):
    '''
    Updates transaction data.

    Takes arguments: transaction_id - required! Data user wants to change (all optional): amount, description, category_id.

    User can update only personal transactions with personal categories.
    '''
    transaction = graphene.Field(TransactionType)

    class Arguments:
        transaction_data = TransactionInput(required=True)

    def mutate(root, info, transaction_data=None):
        user = info.context.user
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
                raise GraphQLError("Can't find category with given category id.")
            transaction.category_id = transaction_data.category_id

        transaction.save()
        return UpdateTransaction(transaction=transaction)

class DeleteTransaction(graphene.Mutation):
    '''
    Delete transactions

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

class CreateCategory(graphene.Mutation):
    '''
    Create a category.

    Takes arguments: amount, description, category_id.

    User can access only personal categories.
    '''
    category = graphene.Field(CategoryType)
    user = graphene.Field(UserType)

    class Arguments:
        name = graphene.String()
        group = graphene.String()

    def mutate(self, info, name, group):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        category = Category(name=name, group=group, user=user)
        category.save()
        return CreateCategory(category=category)

class UpdateCategory(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        category_id = graphene.Int(required=True)
        name = graphene.String()
        group = graphene.NonNull(graphene.String)

    def mutate(self, info, name, group, category_id):
        user = info.context.user
        category = Category.objects.get(id=category_id)
        if category.user != user:
            raise GraphQLError('Not permitted to update this category')
        category.name = name
        category.group = group

        category.save()
        return UpdateCategory(category=category)

class DeleteCategory(graphene.Mutation):
    category_id = graphene.Int()

    class Arguments:
        category_id = graphene.Int(required=True)

    def mutate(self, info, category_id):
        user = info.context.user
        category = Category.objects.get(id=category_id)
        if category.user != user:
            raise GraphQLError("Not permitted to delete this category")
        category.delete()
        return DeleteCategory(category_id=category_id)

class CreateMonth(graphene.Mutation):
    month = graphene.Field(MonthType)
    user = graphene.Field(UserType)

    class Arguments:
        year = graphene.String()
        month = graphene.String()
        start_month_savings = graphene.Int()
        start_month_balance = graphene.Int()

    def mutate(self, info, year, month, start_month_savings, start_month_balance):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        month = Month(
            year=year,
            month=month,
            start_month_balance=start_month_balance,
            start_month_savings=start_month_savings,
            user=user)
        month.save()
        return CreateMonth(month=month)

class UpdateMonth(graphene.Mutation):
    month = graphene.Field(MonthType)

    class Arguments:
        month_id = graphene.Int(required=True)
        start_month_savings = graphene.Int()
        start_month_balance = graphene.Int()

    def mutate(self, info, month_id, start_month_savings, start_month_balance):
        user = info.context.user
        month = Month.objects.get(id=month_id)
        if month.user != user:
            raise GraphQLError('Not permitted to update this month.')
        month.start_month_savings = start_month_savings
        month.start_month_balance = start_month_balance

        month.save()
        return CreateMonth(month=month)


class Mutation(graphene.ObjectType):
    create_transaction = CreateTransaction.Field()
    update_transaction = UpdateTransaction.Field()
    delete_transaction = DeleteTransaction.Field()
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
    create_month = CreateMonth.Field()
    update_month = UpdateMonth.Field()