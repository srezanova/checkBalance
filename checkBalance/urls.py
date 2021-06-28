from django.urls import path, include
from django.contrib import admin
from django.conf import settings

from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

# import debug_toolbar

urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True)), name='graphql'),
    # path('__debug__/', include(debug_toolbar.urls)),
]