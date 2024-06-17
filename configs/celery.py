from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')

app = Celery('configs')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-tasks-due-soon': {
        'task': 'management.tasks.list_tasks_due_in_24_hours',
        'schedule': crontab(minute=0, hour=0),  
    },
}
