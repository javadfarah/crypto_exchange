from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from exchange.utils.set_order import OrderManager
import pytest

from user.models import Balance

User = get_user_model()


@pytest.fixture
def authenticated_client():
    client = APIClient()
    return client


@pytest.fixture
def test_user():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user


@pytest.mark.django_db
def test_my_db():
    count = User.objects.filter().count()
    assert count == 0


@pytest.mark.django_db(transaction=True)
def test_set_order_view_not_enough_balance(test_user, authenticated_client):
    url = reverse('set-order')
    data = {
        'crypto_name': 'Bitcoin',
        'crypto_amount': 5,
        'user_id': test_user.id
    }

    with pytest.raises(Exception) as e_info:
        authenticated_client.post(url, data)


@pytest.mark.django_db(transaction=True)
def test_set_order_view_success(test_user, authenticated_client):
    Balance.objects.create(user=test_user, balance=20)
    url = reverse('set-order')
    data = {
        'crypto_name': 'Bitcoin',
        'crypto_amount': 5,
        'user_id': test_user.id
    }

    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"message": "Order saved and processed"}


def test_set_order_view_invalid_data(test_user, authenticated_client):
    url = reverse('set-order')
    data = {
        'crypto_name': 'Bitcoin',
        'crypto_amount': -5,
        'user_id': test_user.id

    }

    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_buy_from_exchange():
    order_manager = OrderManager(crypto_name="Bitcoin", crypto_amount=5, user_id=1)
    result = order_manager.buy_from_exchange()
    assert result is True
