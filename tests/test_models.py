import pytest

from tests.factories import UserFactory, CategoryFactory
from users.models import CustomUser

#user testing
@pytest.mark.django_db
def test_user_model():
    user = CustomUser.objects.create_user(
        email = 'test@test.com',
        password = 'testpassword',
    )

    assert user.email == 'test@test.com'
    assert user.is_admin == False
    assert user.__str__() == 'test@test.com'

@pytest.mark.django_db
def test_user_no_email():
    with pytest.raises(ValueError):
        user = CustomUser.objects.create_user(
            email = '',
            password = 'testpassword',
        )

@pytest.mark.django_db
def test_user_superuser():
    user = CustomUser.objects.create_superuser(
        email = 'test@test.com',
        password = 'testpassword',
    )

    assert user.email == 'test@test.com'
    assert user.is_admin == True
    assert user.__str__() == 'test@test.com'

@pytest.mark.django_db
def test_user_normalize_email():
    user = CustomUser.objects.create_user(
        email = '   test@TEST.com   ',
        password = 'testpassword',
    )

    assert user.email == 'test@test.com'

#category testing
@pytest.mark.django_db
def test_category_model():
    user = UserFactory(
        email = 'test@test.com',
        password = 'testpassword'
    )

    category = CategoryFactory(
        name = 'dogs',
        group = 'Expense',
        user = user
    )

    assert category.name == 'dogs'
    assert category.group == 'Expense'

    assert category.user == user
    assert category.user.email == "test@test.com"
