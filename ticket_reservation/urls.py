from django.urls import path
from .views import *

urlpatterns = [
    path('', reservation_list, name='reservation_list'),
    path('<int:pk>/', reservation_details, name='reservation_details'),
    # path('stations/', BusStationListCreateView.as_view(), name='bus_station-list-create'),
    # path('stations/<int:pk>/', BusStationDetailView.as_view(), name='bus_station-detail'),
    # path('stops/', BusStopListCreateView.as_view(), name='bus_stop-list-create'),
    # path('stops/<int:pk>/', BusStopDetailView.as_view(), name='busstop-detail'),
]
