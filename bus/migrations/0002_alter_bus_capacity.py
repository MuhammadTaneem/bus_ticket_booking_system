# Generated by Django 4.2.8 on 2023-12-06 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='capacity',
            field=models.IntegerField(),
        ),
    ]
