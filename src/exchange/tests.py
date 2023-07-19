from unittest import mock
from django.urls import reverse
from rest_framework import status
from exchange.utils.set_order import OrderManager
import pytest


class MockedOrderManager(OrderManager):
    def buy_from_exchange(self):
        return False


@pytest.mark.django_db(transaction=True)
def test_set_order_view_not_enough_balance(test_user, authenticated_client):
    url = reverse('set-order')
    data = {
        'crypto_name': 'ABAN',
        'crypto_amount': 5,
        'user_id': test_user.id
    }

    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True)
def test_set_order_view_saved_order(test_user, authenticated_client, add_user_balance):
    url = reverse('set-order')
    data = {
        'crypto_name': 'ABAN',
        'crypto_amount': 1,
        'user_id': test_user.id
    }

    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"message": "Order saved"}


@pytest.mark.django_db(transaction=True)
def test_set_order_view_queue(test_user, authenticated_client, add_user_balance):
    url = reverse('set-order')
    data = {
        'crypto_name': 'ABAN',
        'crypto_amount': 2,
        'user_id': test_user.id
    }

    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"message": "Order saved"}
    url = reverse('set-order')
    data = {
        'crypto_name': 'ABAN',
        'crypto_amount': 1,
        'user_id': test_user.id
    }

    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"message": "Order saved and processed"}


@pytest.mark.django_db(transaction=True)
def test_set_order_view_success(test_user, authenticated_client, add_user_balance):
    url = reverse('set-order')
    data = {
        'crypto_name': 'ABAN',
        'crypto_amount': 5,
        'user_id': test_user.id
    }

    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"message": "Order saved and processed"}


@pytest.mark.django_db(transaction=True)
def test_set_order_view_invalid_data(test_user, authenticated_client):
    url = reverse('set-order')
    data = {
        'crypto_name': 'ABAN',
        'crypto_amount': -5,
        'user_id': test_user.id

    }

    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_buy_from_exchange():
    order_manager = OrderManager(crypto_name="ABAN", crypto_amount=5, user_id=1)
    result = order_manager.buy_from_exchange()
    assert result is True


@pytest.mark.django_db(transaction=True)
@mock.patch("exchange.utils.set_order.OrderManager.buy_from_exchange", side_effect=Exception())
def test_buy_from_exchange_false(self, authenticated_client, test_user, add_user_balance):
    url = reverse('set-order')
    data = {
        'crypto_name': 'ABAN',
        'crypto_amount': 5,
        'user_id': test_user.id

    }

    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data == {'message': 'an error occurred'}
