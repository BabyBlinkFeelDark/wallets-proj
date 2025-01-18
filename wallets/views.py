from django.http import Http404
from rest_framework import generics
from .serializers import (
    WalletSerializer,
    WalletOperationSerializer,
    WalletBalanceSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Wallet, WalletOperation
from django.db import transaction
import uuid


class WalletList(generics.ListCreateAPIView):
    """
    Представление для отображения списка всех кошельков и создания нового кошелька.

    * Если запрос типа GET, возвращает список всех кошельков.
    * Если запрос типа POST, создает новый кошелек.
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления или удаления конкретного кошелька.

    * Если запрос типа GET, извлекает кошелек по ID.
    * Если запрос типа PUT или PATCH, обновляет данные кошелька.
    * Если запрос типа DELETE, удаляет кошелек.
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


@api_view(["POST"])
def create_wallet_operation(request, wallet_uuid):
    """
    Создание операции с кошельком (депозит или вывод средств) для конкретного кошелька.

    Это представление обрабатывает операции депозитов и выводов. Оно выполняет следующие действия:
    - Извлекает кошелек по его UUID.
    - Валидирует тип операции (депозит или вывод) и сумму.
    - При выводе проверяет, достаточно ли средств.
    - Создает операцию и обновляет баланс кошелька.

    Аргументы:
        request (HttpRequest): HTTP-запрос с данными операции.
        wallet_uuid (uuid.UUID): UUID кошелька, с которым выполняется операция.

    Возвращаемое значение:
        Response: Ответ с балансом кошелька после выполнения операции.
    """
    try:
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(id=wallet_uuid)
            serializer = WalletOperationSerializer(data=request.data)
            if serializer.is_valid():
                operation_type = serializer.validated_data["operation_type"]
                amount = serializer.validated_data["amount"]

                if operation_type == "WITHDRAW" and wallet.balance < amount:
                    return Response(
                        {"error": "Insufficient funds"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if operation_type == "DEPOSIT":
                    wallet.balance += amount
                elif operation_type == "WITHDRAW":
                    wallet.balance -= amount

                wallet.save()

                WalletOperation.objects.create(
                    wallet=wallet, operation_type=operation_type, amount=amount
                )

                return Response(
                    {"balance": wallet.balance}, status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Wallet.DoesNotExist:
        return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WalletBalanceDetail(generics.RetrieveAPIView):
    """
    Представление для получения баланса конкретного кошелька.

    Это представление извлекает баланс кошелька по его UUID.

    Аргументы:
        wallet_uuid (uuid.UUID): UUID кошелька.

    Возвращаемое значение:
        Response: Ответ с балансом кошелька.
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletBalanceSerializer

    def get_object(self):
        wallet_uuid = self.kwargs["wallet_uuid"]
        try:
            return Wallet.objects.get(id=wallet_uuid)
        except Wallet.DoesNotExist:
            raise Http404
