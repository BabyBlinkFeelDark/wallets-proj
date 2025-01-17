from email.policy import default

from django.db import models
import uuid

class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    balance = models.DecimalField(max_digits=20, decimal_places=2,default=0)
    def __str__(self):
        return str(self.id)

class WalletOperation(models.Model):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'
    OPERATION_TYPE_CHOICES = [(DEPOSIT,'DEPOSIT'), (WITHDRAW, "WITHDRAW")]
    id = models.AutoField(primary_key = True)
    wallet = models.ForeignKey(Wallet, related_name="operations", on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=10, choices=OPERATION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.operation_type} of {self.amount} to wallet {self.wallet.id}"