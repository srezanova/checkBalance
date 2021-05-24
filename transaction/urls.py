from django.urls import path
from .views import TransactionView, TransactionSingleView

app_name='transactions'

urlpatterns = [
    path('transactions/', TransactionView.as_view()),
    path('transactions/<int:pk>', TransactionSingleView.as_view())

]
