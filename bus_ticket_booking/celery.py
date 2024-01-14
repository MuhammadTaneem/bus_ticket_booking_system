# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings  # Import Django settings module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_ticket_booking.settings')

celery_app = Celery('bus_ticket_booking')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
