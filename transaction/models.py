from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

class Transaction(models.Model):

    GROUP_CHOICES = (
        ('Spending', 'Spending'),
        ('Income', 'Income'),
    )

    user = models.ForeignKey(User, related_name = 'transactions', on_delete=models.CASCADE)
    amount = models.IntegerField()
    created = models.DateField(auto_now=True)
    description = models.CharField(blank=True, max_length=100)
    group = models.CharField(blank=False, choices=GROUP_CHOICES, max_length=8)
    category = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.amount} {self.category} {self.created}'