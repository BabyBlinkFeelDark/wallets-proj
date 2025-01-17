from rest_framework import serializers
from .models import Wallet

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
    operation_type = serializers.ChoiceField(choices=[('DEPOSIT', 'DEPOSIT'), ('WITHDRAW', 'WITHDRAW')])
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)