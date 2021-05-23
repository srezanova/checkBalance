from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from braces.views import SelectRelatedMixin

from . import forms
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()

class TransactionList(LoginRequiredMixin, generic.ListView):
    context_object_name = 'transactions_list'
    model = models.Transaction
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CreateTransaction(LoginRequiredMixin, generic.CreateView):
    form_class = forms.TransactionForm
    model = models.Transaction

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

