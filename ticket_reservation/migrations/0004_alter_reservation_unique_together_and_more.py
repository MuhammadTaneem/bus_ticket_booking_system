# Generated by Django 4.2.8 on 2023-12-27 05:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_reservation', '0003_rename_trip_reservation_schedule_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='bus_seat',
        ),
    ]
