import json
from django.test.testcases import TestCase

from graphene_django.utils.testing import GraphQLTestCase

# class TestCase(GraphQLTestCase):
#     def test_some_query(self):
#         response = self.query(
#             '''
#             query {
#                 CustomUser {
#                     id
#                     email
#                 }
#             }
#             ''',
#             op_name='CustomUser'
#         )

#         content = json.loads(response.content)

#         self.assertResponseNoErrors(response)

class SimpleTest(TestCase):
    def test_cannot_fail(self):
        self.assertEqual(1, 1)

    def test_false_is_false(self):
        self.assertFalse(False)