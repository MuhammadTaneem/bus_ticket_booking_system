from django.urls import path
from .views import (
    BusStationListCreateView,
    BusStationDetailView,
    BusStopListCreateView,
    BusStopDetailView,
    bus_route,
    bus_route_details
)

urlpatterns = [
    path('', bus_route, name='bus_route'),
    path('<int:pk>/', bus_route_details, name='bus_route_details'),
    path('stations/', BusStationListCreateView.as_view(), name='bus_station-list-create'),
    path('stations/<int:pk>/', BusStationDetailView.as_view(), name='bus_station-detail'),
    path('stops/', BusStopListCreateView.as_view(), name='bus_stop-list-create'),
    path('stops/<int:pk>/', BusStopDetailView.as_view(), name='busstop-detail'),
]
