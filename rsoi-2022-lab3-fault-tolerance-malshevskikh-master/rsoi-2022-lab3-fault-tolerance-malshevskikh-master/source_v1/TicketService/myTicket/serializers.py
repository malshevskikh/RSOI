from rest_framework import serializers
from .models import TicketModel

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketModel
        fields = ['id', 'ticket_uid', 'username', 'flight_number', 'price', 'status']
