from django.urls import path
from .views import WalletList, WalletDetail, WalletBalanceDetail

urlpatterns = [
    path('wallets/', WalletList.as_view(), name='wallet-list'),
    path('wallets/<int:pk>/', WalletDetail.as_view(), name='wallet-detail'),
    path('wallets/<uuid:wallet_uuid>/balance/', WalletBalanceDetail.as_view(), name='wallet-balance'),
]
