from collections import OrderedDict
from django.test import RequestFactory, TestCase
from unittest import skip
from graphql import GraphQLError
from graphene.test import Client
from promise.promise import S

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

        self.user1 = CustomUser.objects.create_user(
            email='user1@test.com',
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

        self.transaction1 = TransactionModel.objects.create(
            id=401,
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
        self.user1.delete()
        self.month.delete()
        self.category.delete()
        self.transaction.delete()
        self.transaction1.delete()
        self.plan.delete()

    def test_register_mutation(self):
        query = '''
            mutation {
                register (email:"test@test.com",
                    password1:"testpassword",
                    password2:"testpassword") {
                        success
                }
            }
                '''

        expected = {
            'register': {
                'success': True
            }
        }

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_login_mutation(self):
        query = '''
            mutation {
                login (password:"testpassword", email:"user1@test.com") {
                    success
                }
            }
                '''

        expected = {
            'login': {
                'success': True
            }
        }

        executed = execute_query(query, self.user1)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_create_transaction_mutation(self):
        query = '''
            mutation {
                createTransaction(amount:100, categoryId:300,
                description:"test", monthId:200) {
                    amount
                    description
                    category {
                        id
                    }
                    month {
                        id
                    }
                }
            }
                '''

        expected = OrderedDict([('createTransaction', {
                               'amount': 100, 'description': 'test', 'category': {'id': '300'}, 'month': {'id': '200'}})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_create_transaction_mutation_user1(self):
        query = '''
            mutation {
                createTransaction(amount:100, categoryId:300,
                description:"test", monthId:200) {
                    amount
                    description
                    category {
                        id
                    }
                    month {
                        id
                    }
                }
            }
                '''

        expected = OrderedDict([('createTransaction', {
                               'amount': 100, 'description': 'test', 'category': None, 'month': None})])

        executed = execute_query(query, self.user1)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_create_transactions_mutation_user(self):
        query = '''
            mutation {
                createTransactions(transactions:
                [{amount:100, monthId:200, categoryId:300},
                {amount:200, monthId:200, categoryId:300}]) {
                    transactions {
                        amount
                    }
                }
            }
                '''

        expected = OrderedDict([('createTransactions',
                                 {'transactions': [{'amount': 100}, {'amount': 200}]})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_create_transactions_mutation_user1(self):
        query = '''
            mutation {
                createTransactions(transactions:
                [{amount:100, monthId:200, categoryId:300},
                {amount:200, monthId:200, categoryId:300}]) {
                    transactions {
                        amount
                        category {
                            id
                        }
                        month {
                            id
                        }
                    }
                }
            }
                '''

        expected = OrderedDict([('createTransactions', {'transactions': [
            {'amount': 100, 'category': None, 'month': None},
            {'amount': 200, 'category': None, 'month': None}]})])

        executed = execute_query(query, self.user1)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_update_transaction_mutation(self):
        query = '''
            mutation {
                updateTransaction(id:400,
                description:"TEST") {
                    id
                    description
                }
            }
                '''

        expected = OrderedDict([('updateTransaction',
                                 {'id': '400', 'description': 'TEST'})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_delete_transaction_mutation(self):
        query = '''
            mutation {
                deleteTransaction(id:401) {
                    success
                }
            }
                '''

        expected = OrderedDict([('deleteTransaction', {'success': True})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_create_category_mutation(self):
        query = '''
            mutation {
                createCategory(name:"Stocks", group:Savings) {
                    name
                    group
                }
            }
                '''

        expected = OrderedDict(
            [('createCategory', {'name': 'Stocks', 'group': 'Savings'})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_update_category_mutation(self):
        query = '''
            mutation {
                updateCategory(id:300, name:"Deposit", group:Savings) {
                    name
                    group
                }
            }
                '''

        expected = OrderedDict(
            [('updateCategory', {'name': 'Deposit', 'group': 'Savings'})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_delete_category_mutation(self):
        query = '''
            mutation {
                deleteCategory(id:300) {
                    success
                }
            }
                '''

        expected = OrderedDict([('deleteCategory', {'success': True})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_create_month_mutation(self):
        query = '''
            mutation {
                createMonth(month:December,
                year:A_2021) {
                    month
                    year
                    startMonthSavings
                    startMonthBalance
                }
            }
                '''

        expected = OrderedDict([('createMonth', {
                               'month': 'December',
                               'year': 'A_2021',
                               'startMonthSavings': 0,
                               'startMonthBalance': 0})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_update_month_mutation(self):
        query = '''
            mutation {
                updateMonth(id:200,
                startMonthSavings:1000) {
                    month
                    year
                    startMonthSavings
                    startMonthBalance
                }
            }
                '''

        expected = OrderedDict([('updateMonth', {
                               'month': 'January',
                               'year': 'A_2021',
                               'startMonthSavings': 1000,
                               'startMonthBalance': 100})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        print('')
        print(data)
        self.assertEqual(data, expected)

    def test_create_plan_mutation(self):
        query = '''
            mutation {
                createPlan(monthId:200,
                categoryId:300,
                plannedAmount:1000) {
                    plannedAmount
                }
            }
                '''

        expected = OrderedDict([('createPlan', {'plannedAmount': 1000})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)

    def test_update_plan_mutation(self):
        query = '''
            mutation {
                updatePlan(id:500,
                plannedAmount:777) {
                    id
                    plannedAmount
                }
            }
                '''

        expected = OrderedDict([('updatePlan', {'id': '500', 'plannedAmount': 777})])

        executed = execute_query(query, self.user)
        data = executed.get('data')
        self.assertEqual(data, expected)
