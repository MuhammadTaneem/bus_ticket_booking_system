from django.urls import path
from .views import *

urlpatterns = [
    path('', ScheduleCreate.as_view(), name='schedule-list-create'),
    path('<int:pk>/', schedule_detail_view, name='schedule_detail_view'),
]
