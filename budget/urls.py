from django.urls import path
from .views import CategoryView, GroupView, TransactionSingleView, TransactionView, TotalExpenseView

app_name='budget'

urlpatterns = [
    path('transactions/', TransactionView.as_view()),
    path('transactions/<int:pk>', TransactionSingleView.as_view()),
    path('category/', CategoryView.as_view()),
    path('group/', GroupView.as_view()), 
    path('expenses/', TotalExpenseView.as_view()),
]
