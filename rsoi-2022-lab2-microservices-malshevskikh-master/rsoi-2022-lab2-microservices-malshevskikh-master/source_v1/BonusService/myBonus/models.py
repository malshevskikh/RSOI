from django.db import models
import uuid

# Create your models here.
class PrivilegeModel(models.Model):
    class Privilege(models.TextChoices):
        BRONZE = ("BRONZE", "Bronze")
        SILVER = ("SILVER", "Silver")
        GOLD = ("GOLD", "Gold")
    username = models.CharField(max_length=80, unique=True)
    status = models.CharField(max_length=80, choices=Privilege.choices, default=Privilege.BRONZE)
    balance = models.IntegerField()

    def __str__(self):
        return self.status

class PrivilegeHistoryModel(models.Model):
    class OperationType(models.TextChoices):
        FILL_IN_BALANCE = ("FILL_IN_BALANCE", "fill_in_balance")
        DEBIT_THE_ACCOUNT = ("DEBIT_THE_ACCOUNT", "debit_the_account")
    privilege_id = models.ForeignKey(PrivilegeModel, on_delete=models.CASCADE)
    ticket_uid = models.UUIDField(default=uuid.uuid4, null=False)
    datetime = models.DateTimeField()
    balance_diff = models.IntegerField()
    operation_type = models.CharField(max_length=20, choices=OperationType.choices)

    def __str__(self):
        return self.operation_type
