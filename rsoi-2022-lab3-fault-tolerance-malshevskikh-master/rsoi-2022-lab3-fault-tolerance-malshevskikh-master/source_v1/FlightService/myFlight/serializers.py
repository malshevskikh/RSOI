from rest_framework import serializers
from .models import FlightModel, AirportModel

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirportModel
        fields = ['id', 'name', 'city', 'country']

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightModel
        fields = ['id', 'flight_number', 'datetime', 'from_airport_id', 'to_airport_id', 'price']
