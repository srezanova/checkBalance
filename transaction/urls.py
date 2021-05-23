from django.urls import path
from . import views

app_name='transactions'

urlpatterns = [
    path('', views.TransactionList.as_view(), name="all"),
    path('new/', views.CreateTransaction.as_view(), name="new"),

]
