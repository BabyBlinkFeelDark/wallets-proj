# tests/test_views.py
import uuid
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from wallets.models import Wallet, WalletOperation
from decimal import Decimal

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def wallet(db):
    return Wallet.objects.create(
        id=uuid.uuid4(),
        balance=100.0
    )

@pytest.mark.django_db
class TestWalletViews:

    def test_list_wallets(self, api_client, wallet):
        """
        Тест для получения списка кошельков.
        """
        url = reverse('wallet-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert any(item['id'] == str(wallet.id) for item in response.data)

    def test_create_wallet(self, api_client):
        """
        Тест для создания нового кошелька.
        """
        url = reverse('wallet-list')
        data = {
            "balance": 50.0
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        wallet_id = response.data.get("id")
        assert wallet_id is not None
        assert Wallet.objects.filter(id=wallet_id).exists()

    def test_wallet_detail_retrieve(self, api_client, wallet):
        """
        Тест для получения деталей существующего кошелька.
        """
        url = reverse('wallet-detail', args=[str(wallet.id)])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == str(wallet.id)

    def test_wallet_detail_update(self, api_client, wallet):
        """
        Тест для обновления данных кошелька.
        """
        url = reverse('wallet-detail', args=[str(wallet.id)])
        data = {"balance": 150.0}
        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        wallet.refresh_from_db()
        assert wallet.balance == 150.0

    def test_wallet_detail_delete(self, api_client, wallet):
        """
        Тест для удаления кошелька.
        """
        url = reverse('wallet-detail', args=[str(wallet.id)])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Wallet.objects.filter(id=wallet.id).exists()

    def test_wallet_balance_detail(self, api_client, wallet):
        """
        Тест для получения баланса кошелька.
        """
        url = reverse('wallet-balance', kwargs={'wallet_uuid': str(wallet.id)})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert Decimal(response.data.get('balance')) == wallet.balance

    def test_create_wallet_operation_deposit(self, api_client, wallet):
        """
        Тест для проведения операции депозита (увеличение баланса).
        """
        url = reverse('wallet-operation', kwargs={'wallet_uuid': str(wallet.id)})
        data = {
            "operation_type": "DEPOSIT",
            "amount": 50.0
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        wallet.refresh_from_db()
        assert wallet.balance == 150.0
        operation = WalletOperation.objects.filter(wallet=wallet).last()
        assert operation is not None
        assert operation.operation_type == "DEPOSIT"
        assert operation.amount == 50.0

    def test_create_wallet_operation_withdraw_success(self, api_client, wallet):
        """
        Тест для проведения операции снятия средств, когда средств достаточно.
        """
        url = reverse('wallet-operation', kwargs={'wallet_uuid': str(wallet.id)})
        data = {
            "operation_type": "WITHDRAW",
            "amount": 80.0
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        wallet.refresh_from_db()
        assert wallet.balance == 20.0
        operation = WalletOperation.objects.filter(wallet=wallet).last()
        assert operation is not None
        assert operation.operation_type == "WITHDRAW"
        assert operation.amount == 80.0

    def test_create_wallet_operation_withdraw_insufficient_funds(self, api_client, wallet):
        """
        Тест для проведения операции снятия средств, когда средств недостаточно.
        """
        url = reverse('wallet-operation', kwargs={'wallet_uuid': str(wallet.id)})
        data = {
            "operation_type": "WITHDRAW",
            "amount": 150.0
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        wallet.refresh_from_db()
        assert wallet.balance == 100.0

    def test_create_wallet_operation_wallet_not_found(self, api_client):
        """
        Тест для операции на несуществующем кошельке.
        """
        non_existent_uuid = str(uuid.uuid4())
        url = reverse('wallet-operation', kwargs={'wallet_uuid': non_existent_uuid})
        data = {
            "operation_type": "DEPOSIT",
            "amount": 50.0
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data.get('error') == "Wallet not found"

        def test_create_wallet_operation_invalid_json(api_client, wallet):
            url = reverse('wallet-operation', kwargs={'wallet_uuid': str(wallet.id)})
            data = "invalid_json"
            response = api_client.post(url, data, content_type='application/json')
            assert response.status_code == status.HTTP_400_BAD_REQUEST