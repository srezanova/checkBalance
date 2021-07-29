from django.db import models
from django.core.exceptions import ValidationError

from users.models import CustomUser


class Category(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    color = models.CharField(max_length=50, blank=False, default='gray')


class Month(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    year = models.IntegerField(blank=False)
    month = models.IntegerField(blank=False)
    start_month_savings = models.IntegerField(blank=True, null=True, default=0)
    start_month_balance = models.IntegerField(blank=True, null=True, default=0)

    def validate_month(self, value):
        if value not in range(12):
            raise ValidationError('%s not in range (0,11)' % value)


class Transaction(models.Model):
    GROUP_CHOICES = (
        ('Expense', 'Expense'),
        ('Income', 'Income'),
        ('Savings', 'Savings')
    )
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    group = models.CharField(blank=False, choices=GROUP_CHOICES, max_length=7)
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
