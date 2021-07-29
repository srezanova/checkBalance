from django.test import TestCase
from django.db.utils import IntegrityError
from budget.models import Category, Transaction, Month, Plan

from users.models import CustomUser


class UserModelTest(TestCase):
    '''Tests for CustomUser model'''

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@test.com',
            password='testpassword',
        )

    def test_labels(self):
        field_email_label = self.user._meta.get_field('email').verbose_name
        field_password_label = self.user._meta.get_field(
            'password').verbose_name
        self.assertEqual(field_email_label, 'email address')
        self.assertEqual(field_password_label, 'password')

    def test_email_max_length(self):
        max_length = self.user._meta.get_field('email').max_length
        self.assertEqual(max_length, 254)

    def test_user_detail(self):
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertNotEqual(self.user.password, 'testpassword')
        self.assertFalse(self.user.is_admin)
        self.assertEqual(str(self.user), f'{self.user.email}')

    def test_user_no_email(self):
        with self.assertRaises(ValueError):
            user = CustomUser.objects.create_user(
                email='',
                password='testpassword',
            )

    def test_superuser(self):
        user = CustomUser.objects.create_superuser(
            email='admin@test.com',
            password='testpassword',
        )
        self.assertTrue(user.is_admin)

    def test_duplicated_email(self):
        with self.assertRaises(IntegrityError):
            user = CustomUser.objects.create_user(
                email='test@test.com',
                password='testpassword',
            )

    def test_normalize_email(self):
        user1 = CustomUser.objects.create_user(
            email='   test1@TEST.COM   ',
            password='testpassword',
        )
        self.assertEqual(user1.email, 'test1@test.com')


class BudgetModelTest(TestCase):
    '''Tests for budget model (Category, Transaction, Plan, Month)'''

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@test.com',
            password='testpassword',
        )

        self.category = Category.objects.create(
            user=self.user,
            name='Dogs',
            color='gray',
        )

        self.month = Month.objects.create(
            user=self.user,
            month=1,
            year=2021,
            start_month_savings=100,
            start_month_balance=100,
        )

        self.transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            month=self.month,
            amount=1000,
            description='test',
            group='Expense'
        )

        self.transaction1 = Transaction.objects.create(
            user=self.user,
            category=self.category,
            month=self.month,
            amount=25,
            description='test1',
            group='Expense'
        )

    def test_category(self):
        self.assertEqual(self.category.user.email, 'test@test.com')
        self.assertEqual(self.category.name, 'Dogs')
        self.assertEqual(self.category.color, 'gray')

    def test_month(self):
        self.assertEqual(self.month.user.email, 'test@test.com')
        self.assertEqual(self.month.year, 2021)
        self.assertEqual(self.month.month, 1)
        self.assertEqual(self.month.start_month_savings, 100)
        self.assertEqual(self.month.start_month_balance, 100)

    def test_transaction(self):
        self.assertEqual(self.transaction.user.email, 'test@test.com')
        self.assertEqual(self.transaction.month.month, 1)
        self.assertEqual(self.transaction.month.year, 2021)
        self.assertEqual(self.transaction.category.name, 'Dogs')
        self.assertEqual(self.transaction.amount, 1000)
        self.assertEqual(self.transaction.description, 'test')
        self.assertEqual(self.transaction.group, 'Expense')

    def test_many_to_one_transactions(self):
        self.assertEqual(self.category.transactions.count(), 2)
