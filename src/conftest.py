import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from user.models import Balance

User = get_user_model()


@pytest.fixture(scope='session', autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    django_db_blocker.unblock()


@pytest.fixture
def authenticated_client():
    client = APIClient()
    return client


@pytest.fixture
def test_user():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user


@pytest.fixture
def add_user_balance(test_user):
    Balance.objects.update_or_create(user=test_user, balance=20)


