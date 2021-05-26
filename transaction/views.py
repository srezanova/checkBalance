from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from braces.views import SelectRelatedMixin

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import mixins

from .forms import TransactionForm
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionView(generics.ListCreateAPIView):

    permission_classes = ( IsAuthenticated, )

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user.id)

class TransactionSingleView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = ( IsAuthenticated, )

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user.id)
