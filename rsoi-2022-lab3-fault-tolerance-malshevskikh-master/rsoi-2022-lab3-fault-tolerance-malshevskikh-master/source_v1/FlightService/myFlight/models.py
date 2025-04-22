from django.db import models

# Create your models here.
class AirportModel(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.id


class FlightModel(models.Model):
    flight_number = models.CharField(max_length=20)
    datetime = models.DateTimeField()
    from_airport_id = models.ForeignKey(AirportModel, related_name='from_airport_id', on_delete=models.CASCADE)
    to_airport_id = models.ForeignKey(AirportModel, related_name='to_airport_id', on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return self.flight_number
