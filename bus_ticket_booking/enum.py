from django.db.models import TextChoices


class UserType(TextChoices):
    passenger = 'Passenger'
    ticket_agent = 'Ticket Agent'
    manager = 'Manager'


class BookingStatus(TextChoices):
    pending = 'Pending'
    confirmed = 'Confirmed'
    canceled = 'Canceled'
    ongoing = 'Ongoing'
    done = 'Done'
