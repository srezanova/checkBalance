from django.urls import include, path
from rest_framework import routers
from accounts import views
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('budget.urls')),
    path('auth-rest/', include('rest_auth.urls')),  
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]