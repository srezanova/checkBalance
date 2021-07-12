from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.test.testcases import TestCase
import graphene

from users.models import CustomUser
from budget.models import Category, Transaction, Month, Plan


class QueryModelTest(TestCase):

    def test_should_query_only_fields(self):

        self.category = Category.objects.create(
            name='Dogs',
            group='Expense',
        )

        self.transaction =Transaction.objects.create(
            amount=1000,
            description='test',
            category=self.category
        )

        self.month = Month.objects.create(
            month='January',
            year='2021',
            start_month_savings=100,
            start_month_balance=100,
        )

        class TransactionType(DjangoObjectType):
            id = graphene.ID(source='pk', required=True)
            class Meta:
                model = Transaction
                interfaces = (graphene.relay.Node, )

        class CategoryType(DjangoObjectType):
            id = graphene.ID(source='pk', required=True)
            class Meta:
                model = Category
                interfaces = (graphene.relay.Node, )

        class MonthType(DjangoObjectType):
            id = graphene.ID(source='pk', required=True)
            class Meta:
                model = Month
                interfaces = (graphene.relay.Node, )

        class Query(graphene.ObjectType):
            transactions = graphene.List(TransactionType)
            categories = graphene.List(CategoryType)
            months = graphene.List(MonthType)

            def resolve_transactions(root, info, **kwargs):
                return Transaction.objects.all()

            def resolve_categories(root, info, **kwargs):
                return Category.objects.all()

            def resolve_months(root, info, **kwargs):
                return Month.objects.all()

        schema = graphene.Schema(query=Query)
        query = """
                query {
                transactions {
                    amount
                    description
                    }
                    categories {
                        name
                        group
                        }
                    months {
                        month
                        year
                        startMonthSavings
                        startMonthBalance
                    }
                }
        """

        expected = {
            'transactions':
            [{
                'amount': 1000,
                'description': 'test'
                }],
                'categories':
                [{
                    'name': 'Dogs',
                    'group': 'EXPENSE'
                    }],
                'months':
                [{
                    'month': 'JANUARY',
                    'year': 'A_2021',
                    'startMonthSavings': 100,
                    'startMonthBalance': 100
                    }]
            }

        result = schema.execute(query)

        print(result)
        assert result.data == expected
        assert not result.errors

