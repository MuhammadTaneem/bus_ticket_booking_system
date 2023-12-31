from django.db import models


class BusStation(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class BusStop(models.Model):
    bus_station = models.ForeignKey(BusStation, on_delete=models.CASCADE)
    stops_no = models.IntegerField()
    duration = models.IntegerField()
    distance = models.IntegerField()
    halt = models.IntegerField()

    # route stops_no unique

    def __str__(self):
        return self.bus_station.name


class BusRoute(models.Model):
    name = models.CharField(max_length=255)
    Arrival = models.TimeField()
    Departure = models.TimeField()
    bus_stops = models.ManyToManyField(BusStop)

    def __str__(self):
        return self.name
