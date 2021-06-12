import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Transaction, Category, Month
from graphql import GraphQLError
from users.models import CustomUser

class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser

class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class MonthType(DjangoObjectType):
    class Meta:
        model = Month

class Query(graphene.ObjectType):
    transactions = graphene.List(TransactionType)
    categories = graphene.List(CategoryType)
    months = graphene.List(MonthType)

    def resolve_transactions(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return Transaction.objects.filter(user=user)

    def resolve_categories(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return Category.objects.filter(user=user)

    def resolve_months(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return Month.objects.filter(user=user)

class CreateTransaction(graphene.Mutation):
    transaction = graphene.Field(TransactionType)
    category = graphene.Field(CategoryType)
    user = graphene.Field(UserType)

    class Arguments:
        amount = graphene.NonNull(graphene.Int)
        description = graphene.NonNull(graphene.String)
        category_id = graphene.NonNull(graphene.Int)

    def mutate(self, info, amount, description, category_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        category = Category.objects.get(id=category_id, user=user)
        if not category:
            raise GraphQLError("Can't find category with given category id.")
        transaction = Transaction(amount=amount, description=description, user=user, category=category)
        transaction.save()
        return CreateTransaction(transaction=transaction)

class UpdateTransaction(graphene.Mutation):
    transaction = graphene.Field(TransactionType)

    class Arguments:
        transaction_id = graphene.Int(required=True)
        amount = graphene.NonNull(graphene.Int)
        description = graphene.NonNull(graphene.String)
        category_id = graphene.Int(required=False)

    def mutate(self, info, transaction_id, amount, description, category_id):
        user = info.context.user
        transaction = Transaction.objects.get(id=transaction_id)
        if transaction.user != user:
            raise GraphQLError('Not permitted to update this transaction.')
        transaction.amount = amount
        transaction.description = description
        transaction.category_id = category_id

        transaction.save()
        return UpdateTransaction(transaction=transaction)

class DeleteTransaction(graphene.Mutation):
    transaction_id =  graphene.Int()

    class Arguments:
        transaction_id = graphene.Int(required=True)

    def mutate(self, info, transaction_id):
        user = info.context.user
        transaction = Transaction.objects.get(id=transaction_id)
        if transaction.user != user:
            raise GraphQLError('Not permitted to delete this transaction.')
        transaction.delete()
        return DeleteTransaction(transaction_id=transaction_id)

class CreateCategory(graphene.Mutation):
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
        month = Month(year=year, month=month, start_month_balance=start_month_balance, start_month_savings=start_month_savings, user=user)
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


