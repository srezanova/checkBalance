from django.urls import include, path
from rest_framework import routers
from accounts import views
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('transaction.urls')),
    path('api/token', obtain_auth_token, name = 'obtain_token' ),
    path('rest-auth/', include('rest_auth.urls'))

]