from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Sum
from django.forms.models import model_to_dict

import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import mixins

from .models import Transaction, Group, Category, Month
from .serializers import TransactionSerializer, GroupSerializer, CategorySerializer, TotalSerializer, TotalCategorySerializer, MonthSerializer

class TransactionView(generics.ListCreateAPIView):

    permission_classes = ( IsAuthenticated, )
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user = user.id)

class TransactionSingleView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = ( IsAuthenticated, )
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user = user.id)

class GroupView(generics.ListAPIView):
    permission_classes = ( IsAuthenticated, )
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

class CategoryView(generics.ListCreateAPIView):
    permission_classes = ( IsAuthenticated, )
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(user = user.id)

class TotalView(generics.GenericAPIView):
    permission_classes = ( IsAuthenticated, )

    def get(self, request):
        user = self.request.user
        transaction = Transaction.objects.filter(user = user.id)
        serializer = TotalSerializer(transaction, many=True)
        expense_sum = transaction.filter(group=('2')).aggregate(Sum('amount'))['amount__sum']
        income_sum = transaction.filter(group=('3')).aggregate(Sum('amount'))['amount__sum']
        saving_sum = transaction.filter(group=('4')).aggregate(Sum('amount'))['amount__sum']
        balance = income_sum - saving_sum - expense_sum

        return Response(
                {
                    'total_income': income_sum if income_sum else 0.00, 
                    'total_expenses': expense_sum if expense_sum else 0.00, 
                    'total_savings': saving_sum if saving_sum else 0.00,
                    'balance': balance
                }
            )

class TotalCategoryView(generics.ListAPIView):
    category = Category.objects.all()
    transaction = Transaction.objects.all()
    serializer_class = TotalCategorySerializer
    queryset = Transaction.objects.all()    

class MonthView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = ( IsAuthenticated, )
    serializer_class = MonthSerializer
    queryset = Month.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        return Month.objects.filter(user = user.id)