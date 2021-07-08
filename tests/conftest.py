import pytest
from django.test import Client as BaseClient
from django.urls import reverse
from graphql_jwt.shortcuts import get_token
from django_dynamic_fixture import G

from users.models import CustomUser


class JsonClient(BaseClient):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('user')
        if self.user:
            token = get_token(self.user)
            kwargs['HTTP_AUTHORIZATION'] = 'JWT' + token
        super(JsonClient, self).__init__(*args, **kwargs)

    def _graphql_api_call(self, call_type, field, arguments='', payload=''):
        assert call_type in ('mutation', 'query')
        query = ' %s {%s %s { %s } } ' % (
            call_type,
            field, 
            ('(%s)' % arguments) if arguments else '',
            payload
        )
        return self.post(
            reverse('graphql_api'),
            data={'query': query},
            content_type='application/json'
        )

    def query(self, field, arguments='', payload=''):
        return self._graphql_api_call('query', field, arguments, payload)

    def mutation(self, field, arguments='', payload=''):
        return self._graphql_api_call('mutation', field, arguments, payload)


@pytest.fixture
def user():
    user = G(CustomUser)
    user.set_password('testpassword')
    user.save()
    return user

@pytest.fixture
def client():
    return JsonClient

@pytest.fixture
def auth_client():
    return JsonClient(user=user)