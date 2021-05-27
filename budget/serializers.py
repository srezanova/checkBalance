from rest_framework import serializers
from .models import Transaction, Group, Category # TotalExpense

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TotalExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount']
    
