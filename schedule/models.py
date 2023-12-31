from django.db import models
from bus.models import Bus
from route.models import BusRoute


class Schedule(models.Model):
    name = models.CharField(max_length=200)
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT)
    trip_route = models.ForeignKey(BusRoute, on_delete=models.PROTECT)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    published = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}-{self.arrival_time}'
