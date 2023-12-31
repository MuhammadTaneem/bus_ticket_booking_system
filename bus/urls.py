from django.urls import path
from .views import BusListCreate, bus_detail, bus_seat, bus_seat_details

urlpatterns = [
    path('', BusListCreate.as_view(), name='bus-list-create'),
    path('<int:pk>/', bus_detail, name='bus-detail'),
    path('seats/', bus_seat, name='bus_seat'),
    path('seats/<int:pk>/', bus_seat_details, name='bus_seat_details'),
]
