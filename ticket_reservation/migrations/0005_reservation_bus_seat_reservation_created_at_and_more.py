# Generated by Django 4.2.8 on 2023-12-27 05:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_alter_schedule_end_date_alter_schedule_start_date'),
        ('bus', '0009_alter_bus_capacity'),
        ('ticket_reservation', '0004_alter_reservation_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='bus_seat',
            field=models.ForeignKey(default=12, editable=False, on_delete=django.db.models.deletion.DO_NOTHING, to='bus.busseat'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='last_edit',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('schedule', 'date', 'bus_seat')},
        ),
    ]
