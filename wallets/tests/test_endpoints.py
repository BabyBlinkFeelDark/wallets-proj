from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from wallets.models import Wallet

class WalletTests(APITestCase):
    def test_create_wallet(self):
        url = reverse('wallet-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.count(), 1)
        self.assertEqual(Wallet.objects.get().balance, 0)

    def test_deposit(self):
        wallet = Wallet.objects.create()
        url = reverse('wallet-operation', args=[wallet.id])
        data = {"operation_type": "DEPOSIT", "amount": 1000}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        wallet.refresh_from_db()
        self.assertEqual(wallet.balance, 1000)

    def test_withdraw_insufficient_funds(self):
        wallet = Wallet.objects.create()
        url = reverse('wallet-operation', args=[wallet.id])
        data = {"operation_type": "WITHDRAW", "amount": 1000}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'Insufficient funds')