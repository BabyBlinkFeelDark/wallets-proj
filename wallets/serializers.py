from rest_framework import serializers
from .models import Wallet, WalletOperation

class WalletSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Wallet.

    Этот сериализатор используется для преобразования данных о кошельке в формат JSON
    и обратно.

    Атрибуты:
        model (class): Модель, к которой применяется сериализатор.
        fields (str or list): Список полей, которые будут включены в сериализацию.
    """
    class Meta:
        model = Wallet
        fields = '__all__'


class WalletOperationSerializer(serializers.Serializer):
    """
    Сериализатор для создания операций на кошельке.

    Этот сериализатор используется для валидации данных о типе операции и сумме.
    """
    operation_type = serializers.ChoiceField(choices=[('DEPOSIT', 'DEPOSIT'), ('WITHDRAW', 'WITHDRAW')])
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)

    def validate_amount(self, value):
        """
        Валидация суммы операции.
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value

    def validate_operation_type(self, value):
        """
        Валидация типа операции.
        """
        if value not in ['DEPOSIT', 'WITHDRAW']:
            raise serializers.ValidationError("Invalid operation type.")
        return value


class WalletBalanceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода баланса кошелька.

    Этот сериализатор используется для отображения текущего баланса кошелька.
    """
    class Meta:
        model = Wallet
        fields = ['id', 'balance']
