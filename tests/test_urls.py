from django.urls import reverse, resolve
from django.test import TestCase


class UrlModelTest(TestCase):

    def test_graphql_url(self):
        path = reverse('graphql')
        self.assertEqual(resolve(path).view_name,'graphql')
