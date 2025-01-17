from django.urls import path
from .views import WalletList, WalletDetail, WalletBalanceDetail, create_wallet_operation

urlpatterns = [
    path('wallets/', WalletList.as_view(), name='wallet-list'),
    path('wallets/<uuid:pk>/', WalletDetail.as_view(), name='wallet-detail'),
    path('wallets/<uuid:wallet_uuid>/balance/', WalletBalanceDetail.as_view(), name='wallet-balance'),
    path('wallets/<uuid:wallet_uuid>/operation/', create_wallet_operation, name='wallet-operation'),
]
