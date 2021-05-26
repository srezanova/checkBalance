from django.urls import include, path
from .views import registration_view


urlpatterns = [
    path('register/', registration_view, name = 'register'),
]