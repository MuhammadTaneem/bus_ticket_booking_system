# Generated by Django 4.2.8 on 2023-12-07 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0005_alter_bus_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='capacity',
            field=models.IntegerField(editable=False),
        ),
    ]
