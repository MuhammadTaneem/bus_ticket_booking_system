# tasks.py
from celery import shared_task
from django.utils import timezone
from bus_ticket_booking.enum import BookingStatus
from ticket_reservation.models import TicketReservation
from celery.result import AsyncResult
from bus_ticket_booking.celery import celery_app
from celery.backends.redis import RedisBackend


@shared_task
def cancel_pending_reservation():
    fifteen_minutes_ago = timezone.now() - timezone.timedelta(minutes=15)
    pending_tickets = TicketReservation.objects.filter(status=BookingStatus.pending,
                                                       created_at__lte=fifteen_minutes_ago)
    pending_tickets.update(status=BookingStatus.canceled)


# @shared_task
# def delete_completed_tasks():
#     all_task_results = TaskResult.objects.all()
#     completed_tasks = all_task_results.filter(status__in=['SUCCESS', 'FAILURE'])
#     task_ids = [task.task_id for task in completed_tasks]
#     for task_id in task_ids:
#         print(task_id)
#         result = AsyncResult(task_id, app=celery_app)
#         result.delete()


# from celery.result import AsyncResult
# from your_project_name.celery import celery_app
# from django.db import transaction

# @shared_task
def delete_completed_tasks():
    task_ids = celery_app.backend.client.keys('celery-task-meta-*')
    completed_task_ids = [task_id.decode('utf-8').split('-')[-1] for task_id in task_ids if
                          AsyncResult(task_id.decode('utf-8'), backend=celery_app.backend).status in ['SUCCESS',
                                                                                                      'FAILURE']]
    # for task_id in completed_task_ids:
    #     celery_app.backend.delete(task_id)
    for task_id in completed_task_ids:
        celery_app.backend.delete_result(task_id)
    import pdb;pdb.set_trace()
