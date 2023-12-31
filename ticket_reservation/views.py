from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from bus_ticket_booking.enum import BookingStatus
from .models import TicketReservation
from .serializers import ReservationSerializer  # You need to create a serializer for Reservation


@api_view(['GET', 'POST'])
def reservation_list(request):
    if request.method == 'GET':
        reservations = TicketReservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET,PUT'])
def reservation_details(request, pk):
    try:
        reservation = TicketReservation.objects.get(pk=pk)
    except TicketReservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    elif request.method == 'PUT':
        reservation.status = BookingStatus.canceled
        reservation.save()
