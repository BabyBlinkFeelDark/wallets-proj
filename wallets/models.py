from email.policy import default
from django.db import models
import uuid


class Wallet(models.Model):
    """
    Модель для хранения информации о кошельке пользователя.

    Атрибуты:
        id (UUIDField): Уникальный идентификатор кошелька (primary key).
        balance (DecimalField): Баланс кошелька, с двумя знаками после запятой.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        """
        Возвращает строковое представление объекта Wallet.

        Возвращает:
            str: Идентификатор кошелька.
        """
        return str(self.id)


class WalletOperation(models.Model):
    """
    Модель для учета операций с кошельком.

    Атрибуты:
        DEPOSIT (str): Тип операции для пополнения.
        WITHDRAW (str): Тип операции для вывода средств.
        OPERATION_TYPE_CHOICES (list): Список возможных типов операций.
        id (AutoField): Уникальный идентификатор операции.
        wallet (ForeignKey): Ссылка на кошелек, к которому привязана операция.
        operation_type (CharField): Тип операции (DEPOSIT или WITHDRAW).
        amount (DecimalField): Сумма операции.
        timestamp (DateTimeField): Время проведения операции.
    """

    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    OPERATION_TYPE_CHOICES = [(DEPOSIT, "DEPOSIT"), (WITHDRAW, "WITHDRAW")]

    id = models.AutoField(primary_key=True)
    wallet = models.ForeignKey(
        Wallet, related_name="operations", on_delete=models.CASCADE
    )
    operation_type = models.CharField(max_length=10, choices=OPERATION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Возвращает строковое представление операции.

        Возвращает:
            str: Описание операции с указанием типа, суммы и идентификатора кошелька.
        """
        return f"{self.operation_type} of {self.amount} to wallet {self.wallet.id}"
