from django.urls import path, include
from django.contrib import admin
from django.conf import settings

from graphene_django.views import GraphQLView
from budget.views import CustomGraphQLView
from django.views.decorators.csrf import csrf_exempt

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(CustomGraphQLView.as_view(graphiql=True))),
    path('__debug__/', include(debug_toolbar.urls)),
]