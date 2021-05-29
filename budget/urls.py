from django.urls import path
from .views import CategoryView, GroupView, TransactionSingleView, TransactionView, TotalView, TotalCategoryView, MonthView

app_name='budget'

urlpatterns = [
    path('transactions/', TransactionView.as_view()),
    path('transactions/<int:pk>', TransactionSingleView.as_view()),
    path('user_categories/', CategoryView.as_view()),
    path('group/', GroupView.as_view()), 
    path('total/', TotalView.as_view()),
    path('categories/', TotalCategoryView.as_view()), 
    path('month/<int:pk>', MonthView.as_view()),
]
