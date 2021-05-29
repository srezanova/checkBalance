from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

class Group(models.Model):
    GROUP_CHOICES = (
        ('Expense', 'Expense'),
        ('Income', 'Income'),
        ('Savings', 'Savings')
    )
    name = models.CharField( blank = False, choices = GROUP_CHOICES, max_length = 7, unique = True)

    def __str__(self):
        return self.name

class Category(models.Model):

    user = models.ForeignKey(User, related_name = 'category_transactions', on_delete = models.CASCADE)
    name = models.CharField( max_length = 50, blank = False, unique = True)
    group = models.ForeignKey(Group, related_name = 'group', on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class Transaction(models.Model):

    group = models.ForeignKey(Group, related_name = 'transaction_groups', on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = 'transactions', on_delete = models.CASCADE)
    created = models.DateField(auto_now = True)
    amount = models.DecimalField(max_digits = 8, decimal_places = 2)
    description = models.CharField(blank = True, max_length = 100)
    category = models.ForeignKey(Category, related_name = 'category', on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.amount} {self.category}-{self.group} {self.created}'

class Month(models.Model):
    YEAR_CHOICES = (
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023')
    )
    MONTH_CHOICES = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'), 
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December')
    )
    user = models.ForeignKey(User, related_name = 'months', on_delete = models.CASCADE)
    year = models.CharField(blank = False, choices = YEAR_CHOICES, max_length = 4)
    month = models.CharField(blank = False, choices =  MONTH_CHOICES, max_length = 15)
    start_month_savings = models.DecimalField(max_digits = 8, decimal_places = 2)
    start_month_balance = models.DecimalField(max_digits = 8, decimal_places = 2)

    def __str__(self):
        return f'{self.month} {self.year}'