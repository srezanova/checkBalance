from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .views import CategoryView, TransactionSingleView, TransactionView, TotalView, TotalCategoryView, MonthView

app_name='budget'

urlpatterns = [
    path('transactions/', TransactionView.as_view()),
    path('transactions/<int:pk>', TransactionSingleView.as_view()),
    path('user_categories/', CategoryView.as_view()),
    # path('group/', GroupView.as_view()), 
    path('total/', TotalView.as_view()),
    path('categories/', TotalCategoryView.as_view()), 
    path('month/<int:pk>', MonthView.as_view()),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql = True))),
]
