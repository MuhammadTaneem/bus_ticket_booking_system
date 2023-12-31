from rest_framework import serializers
from .models import Bus, BusSeat


class BusSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusSeat
        fields = ('id', 'row', 'column', 'bus')

    def create(self, validated_data):
        validated_data['row'] = validated_data['row'].upper()
        # return super().create(validated_data)

        if BusSeat.objects.filter(bus=validated_data['bus'], row=validated_data['row'],
                                  column=validated_data['column']).exists():
            raise serializers.ValidationError({'unique error': 'This seat already exists'})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['row'] = validated_data['row'].upper()
        if BusSeat.objects.filter(bus=validated_data['bus'], row=validated_data['row'],
                                  column=validated_data['column']).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({'unique error': 'This seat already exists'})
        return super().update(instance, validated_data)


class BusSerializer(serializers.ModelSerializer):
    seats = BusSeatSerializer(many=True, read_only=True)

    class Meta:
        model = Bus
        fields = (
            'id', 'name', 'number_plate', 'have_ac', 'sleeping_coach', 'double_decker', 'capacity', 'no_of_column',
            'seats')


class BusUpdateSerializer(BusSerializer):
    class Meta:
        model = Bus
        fields = (
            'id', 'name', 'number_plate', 'have_ac', 'sleeping_coach', 'double_decker', 'capacity', 'no_of_column',
            'seats')
        extra_kwargs = {
            'capacity': {'read_only': True}
        }
