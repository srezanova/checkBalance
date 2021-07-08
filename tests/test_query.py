import pytest
from users.models import CustomUser

@pytest.mark.django_db
def test_current_user_query(auth_client):
    
    response = auth_client.query(
        'currentUser',
        payload='id username'
    )

    assert response.status_code == 200