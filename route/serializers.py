from rest_framework import serializers
from .models import *


class BusStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStation
        fields = ('id', 'name')

    def create(self, validated_data):
        if BusStation.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError({'unique error': 'This station already exists'})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if BusStation.objects.filter(name=validated_data['name']).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({'unique error': 'This station already exists'})
        return super().update(instance, validated_data)


class BusStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStop
        fields = ('id', 'bus_station', 'stops_no', 'duration', 'distance', 'halt')


class BusStopListSerializer(serializers.ListSerializer):
    child = BusStopSerializer()


class BusRouteSerializer(serializers.ModelSerializer):
    bus_stops = BusStopSerializer(many=True, read_only=True)
    # bus_stops = BusStopListSerializer(many=True)

    class Meta:
        model = BusRoute
        fields = ('id', 'name', 'Arrival', 'Departure', 'bus_stops')
