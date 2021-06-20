import graphene
from graphene_django import DjangoObjectType, DjangoListField, DjangoConnectionField
from .models import Transaction, Category, Month
from graphql import GraphQLError
from users.models import CustomUser
import graphene_django_optimizer as gql_optimizer


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser

class TransactionType(DjangoObjectType):
    '''
    query One Category to Many Transactions
    '''
    categories = graphene.List('budget.schema.CategoryType')
    
    class Meta:
        model = Transaction
        use_connection = True
    
    def resolve_categories(root, info, **kwargs):
        user = info.contex.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return info.contex.categories_by_transaction_ids_loader.load(root.id)

class CategoryType(DjangoObjectType):
    '''
    query Many Transactions to One Category for each Transaction
    '''
    transactions = graphene.List('budget.schema.TransactionType')

    class Meta:
        model = Category
        use_connection = True

    def resolve_transactions(root, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return info.context.transactions_by_category_id_loader.load(root.id)
        
class MonthType(DjangoObjectType):
    class Meta:
        model = Month

class Query(graphene.ObjectType):

    categories = DjangoConnectionField(CategoryType)
    months = graphene.List(MonthType)
    transactions = DjangoConnectionField(TransactionType)

    def resolve_transactions(root, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return Transaction.objects.filter(user=user)

    def resolve_categories(root, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return Category.objects.filter(user=user)

    def resolve_months(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You need to be logged in.')
        return Month.objects.filter(user=user)

