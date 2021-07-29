import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
import graphene_django_optimizer as gql_optimizer

from budget.models import Transaction as TransactionModel
from budget.models import Category as CategoryModel
from budget.models import Month as MonthModel


class GroupChoice(graphene.Enum):
    Expense = 'Expense'
    Income = 'Income'
    Savings = 'Savings'


class Transaction(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = TransactionModel
        description = "Type definition for a single transaction."
        exclude = ['user']

    created_at = graphene.String()


class Query(graphene.ObjectType):

    transaction = graphene.Field(Transaction,
                                 id=graphene.ID(required=True),
                                 description='Date format for "createdAt field" - YYYY-MM-DD')

    transactions = graphene.List(Transaction,
                                 created_at=graphene.String(),
                                 category=graphene.ID(),
                                 month=graphene.ID(),
                                 group=GroupChoice())

    def resolve_transaction(self, info, id):
        '''Resolves single transaction'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        try:
            transaction = TransactionModel.objects.get(id=id, user=user)
        except TransactionModel.DoesNotExist:
            return None

        return transaction

    def resolve_transactions(self,
                             info,
                             group=None,
                             created_at=None,
                             category=None,
                             month=None,):
        '''Resolves transactions.'''
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Unauthorized.')

        category_id = category
        month_id = month

        if category_id is not None:
            try:
                category = CategoryModel.objects.get(
                    id=category_id)
            except CategoryModel.DoesNotExist:
                return []

        if month_id is not None:
            try:
                month = MonthModel.objects.get(id=month_id)
            except MonthModel.DoesNotExist:
                return []

        # saving passed args for filter and deleting fields we cannot pass in filter
        saved_args = locals()
        del saved_args['self']
        del saved_args['info']
        del saved_args['category_id']
        del saved_args['month_id']

        # creating new dict with not None args
        saved_args = {k: v for k, v in saved_args.items() if v is not None}

        return gql_optimizer.query(TransactionModel.objects.filter(**saved_args), info)
