from django.http import Http404
from rest_framework import generics
from .serializers import WalletSerializer, WalletOperationSerializer, WalletBalanceSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Wallet, WalletOperation
from django.db import transaction
import uuid


class WalletList(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


@api_view(['POST'])
def create_wallet_operation(request, wallet_uuid):
    # Преобразование wallet_uuid в объект UUID
    if not isinstance(wallet_uuid, uuid.UUID):
        try:
            wallet_uuid = uuid.UUID(wallet_uuid)
        except ValueError:
            return Response({'error': 'Invalid wallet UUID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            # Получение кошелька с блокировкой на запись
            wallet = Wallet.objects.select_for_update().get(id=wallet_uuid)

            # Валидация данных операции
            serializer = WalletOperationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            operation_type = serializer.validated_data['operation_type']
            amount = serializer.validated_data['amount']

            # Логика операций
            if operation_type == 'WITHDRAW' and wallet.balance < amount:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

            if operation_type == 'DEPOSIT':
                wallet.balance += amount
            elif operation_type == 'WITHDRAW':
                wallet.balance -= amount

            wallet.save()

            # Сохранение операции
            WalletOperation.objects.create(wallet=wallet, operation_type=operation_type, amount=amount)

            return Response({'balance': wallet.balance}, status=status.HTTP_201_CREATED)

    except Wallet.DoesNotExist:
        return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)
