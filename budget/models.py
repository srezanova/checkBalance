from django.db import models
from django.contrib.auth import get_user_model

class Category(models.Model):
    GROUP_CHOICES = (
        ('Expense', 'Expense'),
        ('Income', 'Income'),
        ('Savings', 'Savings')
    )
    user = models.ForeignKey(get_user_model(), null=True, on_delete = models.CASCADE)
    name = models.CharField( max_length = 50, blank = False)
    group = models.CharField(blank = False, choices = GROUP_CHOICES, max_length = 7)

    def __str__(self):
        return f'{self.name} {self.user} {self.group}'

class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, on_delete = models.CASCADE)
    created = models.DateField(auto_now_add = True)
    amount = models.IntegerField()
    description = models.CharField(null = True, blank = True, max_length = 100)
    category = models.ForeignKey(Category, related_name = 'categories', null=True, on_delete = models.SET_NULL)

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
    
    user = models.ForeignKey(get_user_model(), null=True, on_delete = models.CASCADE)
    year = models.CharField(blank = False, choices = YEAR_CHOICES, max_length = 4)
    month = models.CharField(blank = False, choices =  MONTH_CHOICES, max_length = 15)
    start_month_savings = models.IntegerField()
    start_month_balance = models.IntegerField()

