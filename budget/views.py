from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Sum


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import mixins

from .models import Transaction, Group, Category #TotalExpense
from .serializers import TransactionSerializer, GroupSerializer, CategorySerializer, TotalExpenseSerializer

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

class CategoryView(generics.ListAPIView):
    permission_classes = ( IsAuthenticated, )
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(user = user.id)

class TotalExpenseView(generics.GenericAPIView):
    serializer_class = TotalExpenseSerializer
    queryset = Transaction.objects.all()

    def get(self, request):
        user = self.request.user
        transaction = Transaction.objects.filter(user = user.id)
        serializer = TotalExpenseSerializer(transaction, many=True)
        expense_sum = transaction.filter(group=('2')).aggregate(Sum('amount'))['amount__sum']
        income_sum = transaction.filter(group=('3')).aggregate(Sum('amount'))['amount__sum']
        balance = income_sum - expense_sum
        return Response(
                {
                    'Total Income': income_sum if income_sum else 0.00, 
                    'Total Expenses': expense_sum if expense_sum else 0.00, 
                    'Balance': balance
                }
            )


