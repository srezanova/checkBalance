from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.test.testcases import TestCase
import graphene

from users.models import CustomUser
from budget.models import Category, Transaction, Month, Plan



class QueryModelTest(TestCase):

    def test_should_query_only_fields(self):

        self.transaction =Transaction.objects.create(
            amount=1000,
            description='test',
        )

        class TransactionType(DjangoObjectType):
            id = graphene.ID(source='pk', required=True)
            class Meta:
                model = Transaction
                interfaces = (graphene.relay.Node, )


        class Query(graphene.ObjectType):
            transactions = graphene.List(TransactionType)

            def resolve_transactions(root, info, **kwargs):
                return Transaction.objects.all()

        schema = graphene.Schema(query=Query)
        query = """
            query {
            transactions {
                amount
                description
                }
            }
        """
        result = schema.execute(query)
        assert result.data == {'transactions': [{'amount': 1000, 'description': 'test'}]}

