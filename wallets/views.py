from django.http import Http404
from rest_framework import generics
from .serializers import WalletSerializer, WalletOperationSerializer, WalletBalanceSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Wallet, WalletOperation
from django.db import transaction


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


@api_view(['POST'])
def create_wallet_operation(request, wallet_uuid):
    """
    Создание операции для конкретного кошелька (депозит или снятие средств).

    Проверяет тип операции (DEPOSIT/WITHDRAW), выполняет валидацию суммы
    и выполняет изменения на кошельке, создавая запись о операции.

    Параметры:
        request (Request): HTTP запрос с данными для операции.
        wallet_uuid (str): UUID кошелька, к которому привязана операция.

    Ответ:
        balance (float): Новый баланс кошелька после выполнения операции.
        error (str): Сообщение об ошибке, если операция не может быть выполнена.
    """
    wallet = Wallet.objects.filter(id=wallet_uuid).first()
    if not wallet:
        return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = WalletOperationSerializer(data=request.data)
    if serializer.is_valid():
        operation_type = serializer.validated_data['operation_type']
        amount = serializer.validated_data['amount']

        if operation_type == 'WITHDRAW' and wallet.balance < amount:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            if operation_type == 'DEPOSIT':
                wallet.balance += amount
            elif operation_type == 'WITHDRAW':
                wallet.balance -= amount

            wallet.save()

            WalletOperation.objects.create(wallet=wallet, operation_type=operation_type, amount=amount)

        return Response({'balance': wallet.balance}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WalletBalanceDetail(generics.RetrieveAPIView):
    """
    Представление для получения баланса конкретного кошелька.
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletBalanceSerializer

    def get_object(self):
        wallet_uuid = self.kwargs['wallet_uuid']
        try:
            return Wallet.objects.get(id=wallet_uuid)
        except Wallet.DoesNotExist:
            raise Http404