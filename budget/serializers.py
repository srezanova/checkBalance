from rest_framework import serializers
from .models import Transaction, Category, Month

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount']
    
class TotalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['category', 'amount']

class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Month
        fields = '__all__'