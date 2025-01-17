import pytest
from rest_framework import status
from rest_framework.test import APIClient
from wallets.models import Wallet
from django.urls import reverse


@pytest.fixture
def wallet():
    """
    Создание кошелька для использования в тестах.
    """
    return Wallet.objects.create(balance=100.00)


@pytest.fixture
def api_client():
    """
    API клиент для выполнения запросов.
    """
    return APIClient()


@pytest.mark.django_db
def test_create_wallet(api_client):
    """
    Тест для создания нового кошелька.
    """
    url = reverse('wallet-list')
    data = {"balance": 0.00}

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data
    assert response.data['balance'] == 0.00



