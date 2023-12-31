from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import BusStation, BusStop, BusRoute
from .serializers import BusStationSerializer, BusStopSerializer, BusRouteSerializer, BusStopListSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class BusStationListCreateView(generics.ListCreateAPIView):
    queryset = BusStation.objects.all()
    serializer_class = BusStationSerializer


class BusStationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusStation.objects.all()
    serializer_class = BusStationSerializer


class BusStopListCreateView(generics.ListCreateAPIView):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer


class BusStopDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer


# class BusRouteListCreateView(generics.ListCreateAPIView):
#     queryset = BusRoute.objects.all()
#     serializer_class = BusRouteSerializer
#
#
# class BusRouteDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = BusRoute.objects.all()
#     serializer_class = BusRouteSerializer


# from .models import BusStop, BusRoute
# from .serializers import BusStopSerializer, BusRouteSerializer

@api_view(['POST','GET'])
def bus_route(request):
    if request.method == 'POST':
        stops_data = request.data.get('bus_stops', [])
        route_data = request.data.get('bus_route', {})
        stops_serializer = BusStopSerializer(data=stops_data, many=True)
        if stops_serializer.is_valid():
            stops_serializer.save()
            created_stops_ids = [stop['id'] for stop in stops_serializer.data]
            route_serializer = BusRouteSerializer(data={**route_data})
            if route_serializer.is_valid():
                route = route_serializer.save()
                route.bus_stops.set(created_stops_ids)
                return Response(route_serializer.data, status=status.HTTP_201_CREATED)
            else:
                BusStop.objects.filter(id__in=[stop['id'] for stop in stops_serializer.data]).delete()
                return Response(route_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(stops_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        queryset = BusRoute.objects.all()
        # serializer = BusRouteSerializer(queryset,many=True)
        # return Response(serializer.data)
        paginator = PageNumberPagination()
        paginator.page_size = request.GET.get('page_size', 10)
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = BusRouteSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def bus_route_details(request, pk):
    try:
        route = BusRoute.objects.get(pk=pk)
    except BusRoute.DoesNotExist:
        return Response({'error': 'BusRoute does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BusRouteSerializer(route)
        return Response(serializer.data)

    elif request.method == 'PUT':
        stops_data = request.data.get('bus_stops', [])
        route_data = request.data.get('bus_route', {})

        # Serialize and update bus stops
        stops_serializer = BusStopSerializer(instance=route.bus_stops.all(), data=stops_data,many=True)
        import pdb;pdb.set_trace()
        if stops_serializer.is_valid():
            stops_serializer.save()


            # Update bus route data
            route_serializer = BusRouteSerializer(instance=route, data=route_data)
            if route_serializer.is_valid():
                route_serializer.save()
                return Response(route_serializer.data, status=status.HTTP_200_OK)
            else:
                # If there's an issue with the route update, rollback stops to previous state
                stops_serializer.save()  # This will revert changes to stops
                return Response(route_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(stops_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the associated bus stops
        route.bus_stops.all().delete()
        # Delete the bus route
        route.delete()
        return Response({'message': f'BusRoute with ID {pk} and its associated bus stops have been deleted.'},
                        status=status.HTTP_204_NO_CONTENT)
