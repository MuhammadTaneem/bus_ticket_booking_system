from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from schedule.models import Schedule
from tauth.permission import IsManager
from .models import Bus, BusSeat
from .serializers import BusSerializer, BusUpdateSerializer, BusSeatSerializer
from rest_framework import serializers


class BusListCreate(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [IsManager]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsManager])
def bus_detail(request, pk):
    bus = get_object_or_404(Bus, id=pk)
    bus_seats = BusSeat.objects.filter(bus=bus)
    if request.method == 'GET':
        bus_details = {
            'bus': {
                'id': bus.id,
                'name': bus.name,
                'number_plate': bus.number_plate,
                'have_ac': bus.have_ac,
                'sleeping_coach': bus.sleeping_coach,
                'double_decker': bus.double_decker,
                'capacity': bus.capacity,
                'no_of_column': bus.no_of_column
            },
            'seats': [
                {
                    'id': seat.id,
                    'row': seat.row,
                    'column': seat.column
                }
                for seat in bus_seats
            ]
        }
        return Response(bus_details)

    elif request.method == 'PUT':
        serializer = BusUpdateSerializer(bus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        for seat in bus_seats:
            seat.delete()
        bus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsManager])
def bus_seat(request):
    if request.method == 'POST':
        serializer = BusSeatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsManager])
def bus_seat_details(request, pk):
    if request.method == 'GET':
        seat = get_object_or_404(BusSeat, pk=pk)
        serializer = BusSeatSerializer(seat)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        seat = get_object_or_404(BusSeat, pk=pk)
        schedule = Schedule.objects.filter(bus=seat.bus)
        if schedule is None:
            seat.delete()
        return Response({'details': 'This seat already have a schedule'})
    # elif request.method == 'PUT':
    #     seat = get_object_or_404(BusSeat, pk=pk)
    #     schedule = Schedule.objects.filter(bus=seat.bus).exists()
    #     if not schedule:
    #         serializer = BusSeatSerializer(seat, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #     return Response({'details': 'This seat already have a schedule'})

    elif request.method == 'PUT':
        seat = get_object_or_404(BusSeat, pk=pk)
        schedule = Schedule.objects.filter(bus=seat.bus).exists()

        if not schedule:

            # try:
            #     # import pdb;pdb.set_trace()
            #     serializer = BusSeatSerializer(seat, data=request.data)
            #     serializer.is_valid(raise_exception=True)
            #     serializer.save()
            #     return Response(serializer.data)
            # except serializers.ValidationError as e:
            #     return Response({'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            serializer = BusSeatSerializer(seat, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'details': 'This seat already has a schedule'})
