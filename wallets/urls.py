from django.urls import path
from .views import WalletList, WalletDetail

urlpatterns = [
    path('wallets/', WalletList.as_view(), name='wallet-list'),
    path('wallets/<int:pk>/', WalletDetail.as_view(), name='wallet-detail'),
]
