from django.db import models
from users.models import CustomUser


class Category(models.Model):
    GROUP_CHOICES = (
        ('Expense', 'Expense'),
        ('Income', 'Income'),
        ('Savings', 'Savings')
    )
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    group = models.CharField(blank=False, choices=GROUP_CHOICES, max_length=7)


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

    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    year = models.CharField(blank=False, choices=YEAR_CHOICES, max_length=4)
    month = models.CharField(blank=False, choices=MONTH_CHOICES, max_length=15)
    start_month_savings = models.IntegerField(blank=True, null=True)
    start_month_balance = models.IntegerField(blank=True, null=True)


class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    amount = models.IntegerField()
    description = models.CharField(null=True, blank=True, max_length=100)
    category = models.ForeignKey(
        Category, related_name='transactions', null=True, on_delete=models.SET_NULL)
    month = models.ForeignKey(
        Month, related_name='transactions', null=True, on_delete=models.SET_NULL)


class Plan(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    planned_amount = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(
        Category, blank=False, related_name='plan', null=True, on_delete=models.SET_NULL)
    month = models.ForeignKey(
        Month, blank=False, related_name='plan', null=True, on_delete=models.SET_NULL)
