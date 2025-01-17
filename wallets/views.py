from django.shortcuts import render
from rest_framework import generics
from .models import Wallet
from .serializers import WalletSerializer

class WalletList(generics.ListCreateAPIView):
    """
    Представление для получения списка всех кошельков и создания нового.

    Атрибуты:
        queryset (QuerySet): Все кошельки, которые могут быть использованы в API.
        serializer_class (class): Сериализатор для преобразования данных в формат JSON.
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

class WalletDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления или удаления конкретного кошелька.

    Атрибуты:
        queryset (QuerySet): Один кошелек, который будет обработан.
        serializer_class (class): Сериализатор для преобразования данных в формат JSON.
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

