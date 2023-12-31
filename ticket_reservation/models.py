import datetime

from celery import shared_task
from django.db import models

from bus_ticket_booking.enum import BookingStatus
from schedule.models import Schedule
from bus.models import BusSeat
from route.models import BusStop
from django.contrib.auth import get_user_model

User = get_user_model()


class TicketReservation(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    passenger = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    bus_seat = models.ForeignKey(BusSeat, on_delete=models.DO_NOTHING)
    departure_stop = models.ForeignKey(BusStop, on_delete=models.DO_NOTHING, related_name='reservation_start')
    arrival_stop = models.ForeignKey(BusStop, on_delete=models.DO_NOTHING, related_name='reservation_end')
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.pending)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('schedule', 'date', 'bus_seat')

    def __str__(self):
        return f"{self.schedule.name}: by: {self.passenger} [departure:{self.departure_stop}] [arrival:{self.arrival_stop}]"


from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from datetime import timedelta


@receiver(post_save, sender=TicketReservation)
def schedule_ticket_cancellation(sender, instance, created, **kwargs):
    if created and instance.status == 'pending':
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=15,  # Set to 15 minutes
        )
        PeriodicTask.objects.create(
            crontab=schedule,
            name=f"Cancel reservation {instance.id} if still pending",
            task='your_app.tasks.cancel_pending_reservation',
            args=[instance.id],
        )


@shared_task
def cancel_pending_reservation(ticket_id):
    ticket = TicketReservation.objects.get(id=ticket_id)
    if ticket.status == BookingStatus.pending:
        ticket.status = BookingStatus.canceled
    ticket.save()
