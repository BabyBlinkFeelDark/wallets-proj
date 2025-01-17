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

# wallets/views.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Wallet, WalletOperation
from .serializers import WalletOperationSerializer
from django.db import transaction

@api_view(['POST'])
def create_wallet_operation(request, wallet_uuid):
    wallet = Wallet.objects.filter(id=wallet_uuid).first()
    serializer = WalletOperationSerializer(data=request.data)
    if serializer.is_valid():
        operation_type = serializer.validated_data['operation_type']
        amount = serializer.validated_data['amount']
        with transaction.atomic():
            if operation_type == 'DEPOSIT':
                wallet.balance += amount
            elif operation_type == 'WITHDRAW':
                wallet.balance -= amount
            wallet.save()
            WalletOperation.objects.create(wallet=wallet, operation_type=operation_type, amount=amount)
        return Response({'balance': wallet.balance}, status=status.HTTP_201_CREATED)

