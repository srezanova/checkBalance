from django.test import RequestFactory, TestCase
from unittest import skip
from graphql import GraphQLError
from graphene.test import Client

from users.models import CustomUser
from budget.models import Transaction as TransactionModel
from budget.models import Category as CategoryModel
from budget.models import Month as MonthModel
from budget.models import Plan as PlanModel
from checkBalance.schema import schema


TestCase.maxDiff = None


def execute_query(query, user=None, variable_values=None, **kwargs):
    """
    Returns the results of executing a graphQL query using the graphene test client.
    """
    task_factory = RequestFactory()
    context_value = task_factory.get('/graphql/')
    context_value.user = user
    client = Client(schema)
    executed = client.execute(
        query, context_value=context_value, variable_values=variable_values, **kwargs)
    return executed


class QueryTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            id=100,
            email='user@test.com',
            password='testpassword',
        )

        self.month = MonthModel.objects.create(
            id=200,
            user=self.user,
            month='January',
            year='2021',
            start_month_savings=100,
            start_month_balance=100,
        )

        self.category = CategoryModel.objects.create(
            id=300,
            user=self.user,
            name='Dogs',
            group='Expense',
        )

        self.transaction = TransactionModel.objects.create(
            id=400,
            user=self.user,
            category=self.category,
            month=self.month,
            amount=1000,
            description='test',
        )

        self.plan = PlanModel.objects.create(
            id=500,
            user=self.user,
            category=self.category,
            month=self.month,
            planned_amount=10,
        )

    def tearDown(self):
        self.user.delete()
        self.month.delete()
        self.category.delete()
        self.transaction.delete()
        self.plan.delete()

    def test_me_query(self):
        query = '''
                query {
                    me {
                        id
                        email
                    }
                }
                '''

        expected = {'me': {
            'id': '100',
            'email': 'user@test.com',
        }}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_categories_query(self):
        query = '''
            query {
                categories {
                    id
                    name
                    group
                }
            }
                '''

        expected = {'categories': [
            {'id': '300', 'name': 'Dogs', 'group': 'EXPENSE'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_categories_filter_query(self):
        query = '''
            query {
                categories (id:300, name:"Dogs", group:Expense) {
                    id
                    name
                    group
                }
            }
                '''

        expected = {'categories': [
            {'id': '300', 'name': 'Dogs', 'group': 'EXPENSE'}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_months_query(self):
        query = '''
            query {
                months {
                    id
                    month
                    year
                    startMonthSavings
                    startMonthBalance
                }
            }
                '''

        expected = {'months': [
            {'id': '200', 'month': 'JANUARY',
             'year': 'A_2021', 'startMonthSavings': 100, 'startMonthBalance': 100}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_month_query(self):
        query = '''
            query {
                month(id:200) {
                    id
                }
            }
                '''

        expected = {'month': {'id': '200'}}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_category_query(self):
        query = '''
            query {
                category(id:300) {
                    id
                }
            }
                '''

        expected = {'category': {'id': '300'}}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_transaction_query(self):
        query = '''
            query {
                transaction(id:400) {
                    id
                }
            }
                '''

        expected = {'transaction': {'id': '400'}}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_plan_query(self):
        query = '''
            query {
                plan(id:500) {
                    id
                }
            }
                '''

        expected = {'plan': {'id': '500'}}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_months_filter_query(self):
        query = '''
            query {
                months (id:200, month:January, year:A_2021) {
                    id
                    month
                    year
                    startMonthSavings
                    startMonthBalance
                }
            }
                '''

        expected = {'months': [
            {'id': '200', 'month': 'JANUARY',
             'year': 'A_2021', 'startMonthSavings': 100, 'startMonthBalance': 100}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_transactions_query(self):
        query = '''
            query {
                transactions {
                    id
                    amount
                    description
                    month {
                    id
                    }
                    category {
                    id
                    }
                }
            }
                '''

        expected = {'transactions': [{'id': '400', 'amount': 1000, 'description': 'test', 'month': {
            'id': '200'}, 'category': {'id': '300'}}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_transactions_filter_query(self):
        query = '''
            query {
                transactions(id:400, amount:1000) {
                    id
                    amount
                    description
                    month {
                    id
                    }
                    category {
                    id
                    }
                }
            }
                '''

        expected = {'transactions': [{'id': '400', 'amount': 1000, 'description': 'test', 'month': {
            'id': '200'}, 'category': {'id': '300'}}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_plans_query(self):
        query = '''
            query {
                plans {
                    id
                    plannedAmount
                    month {
                        id
                    }
                    category {
                        id
                    }
                }
            }
                '''

        expected = {'plans': [
            {'id': '500', 'plannedAmount': 10,
             'month': {'id': '200'},
             'category': {'id': '300'}}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_plans_filter_query(self):
        query = '''
            query {
                plans (id:500, categoryId:300, monthId:200){
                    id
                    plannedAmount
                    month {
                        id
                    }
                    category {
                        id
                    }
                }
            }
                '''

        expected = {'plans': [
            {'id': '500', 'plannedAmount': 10,
             'month': {'id': '200'},
             'category': {'id': '300'}}]}

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)
