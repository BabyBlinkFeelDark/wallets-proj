from django.urls import path
from .views import (
    WalletList,
    WalletDetail,
    WalletBalanceDetail,
    create_wallet_operation,
)

urlpatterns = [
    path("api/v1/wallets/", WalletList.as_view(), name="wallet-list"),
    path("api/v1/wallets/<uuid:pk>/", WalletDetail.as_view(), name="wallet-detail"),
    path(
        "api/v1/wallets/<uuid:wallet_uuid>/",
        WalletBalanceDetail.as_view(),
        name="wallet-balance",
    ),
    path(
        "api/v1/wallets/<uuid:wallet_uuid>/operation/",
        create_wallet_operation,
        name="wallet-operation",
    ),
]
