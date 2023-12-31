from rest_framework import serializers
from .models import TicketReservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReservation
        fields = '__all__'
