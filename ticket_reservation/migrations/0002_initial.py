# Generated by Django 4.2.8 on 2023-12-06 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ticket_reservation', '0001_initial'),
        ('schedule', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='passenger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reservation',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.schedule'),
        ),
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('trip', 'date', 'bus_seat')},
        ),
    ]
