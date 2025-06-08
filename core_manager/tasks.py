from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from core_manager.models.borrowing import Borrowing
from .services.notification import NotificationService

@shared_task
def send_borrowing_confirmation(borrowing_ids):
    """Send confirmation email for borrowed books"""
    borrowings = Borrowing.objects.filter(id__in=borrowing_ids)
    NotificationService.send_borrowing_confirmation(borrowings)

@shared_task
def check_due_books():
    """Check for books due in the next 3 days and send reminders"""
    three_days_from_now = timezone.now() + timedelta(days=3)
    due_borrowings = Borrowing.objects.filter(
        status='active',
        due_date__lte=three_days_from_now,
        due_date__gt=timezone.now()
    )

    for borrowing in due_borrowings:
        NotificationService.send_return_reminder(borrowing) 
