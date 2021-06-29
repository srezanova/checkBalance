import pytest
from django.urls import reverse, resolve

class TestUrls:

    def test_graphql_url(self):
        path = reverse('graphql')
        assert resolve(path).view_name == 'graphql'
