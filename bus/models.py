from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Bus(models.Model):
    name = models.CharField(max_length=200)
    number_plate = models.CharField(max_length=200)
    have_ac = models.BooleanField(default=False)
    sleeping_coach = models.BooleanField(default=False)
    double_decker = models.BooleanField(default=False)
    capacity = models.IntegerField()
    no_of_column = models.IntegerField()

    def __str__(self):
        return f"{self.name}: {self.capacity} seats"


class BusSeat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    row = models.CharField()
    column = models.IntegerField()

    class Meta:
        unique_together = ('bus', 'row', 'column')

    def __str__(self):
        return f"{self.bus.name} {self.row} {self.column}"


@receiver(post_save, sender=Bus)
def populate_bus_seats(sender, instance, created, **kwargs):
    if not created:
        return
    for i in range(instance.capacity):
        row = chr(65 + i // instance.no_of_column)
        col = i % instance.no_of_column + 1
        BusSeat.objects.create(bus=instance, row=row, column=col)
