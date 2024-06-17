from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone  # Use timezone from Django
from datetime import timedelta
from .models import Task

@shared_task
def list_tasks_due_in_24_hours(recipient_list_emails):
    now = timezone.now() 
    due_in_24_hours = now + timedelta(hours=24)
    tasks = Task.objects.filter(due_date__lte=due_in_24_hours)
    
    for task in tasks:
        subject = f'Reminder for task: {task.title}'
        message = f'Hello,\n\nThis is a reminder to check your task:\n\n{task.title}\n\nDue Date: {task.due_date}\n\nPlease take action accordingly.'
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list_emails,  
            fail_silently=False,
        )


# @shared_task
# def add(x, y):
#     return x + y