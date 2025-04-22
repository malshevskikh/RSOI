from django.db import models
import uuid


# Create your models here.
class TicketModel(models.Model):
    # id = models.AutoField(primary_key=True)
    ticket_uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=80)
    flight_number = models.CharField(max_length=20)
    price = models.IntegerField()

    class StatusOfFlight(models.TextChoices):
        PAID = ("PAID", "Paid")
        RETURNED = ("CANCELED", "Canceled")

    status = models.CharField(max_length=20, choices=StatusOfFlight.choices)

    def __str__(self):
        return self.ticket_uid
