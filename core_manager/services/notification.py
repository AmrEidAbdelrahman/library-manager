from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from typing import List
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from core_manager.models.borrowing import Borrowing

class NotificationService:
    @staticmethod
    def send_borrowing_confirmation(borrowings: List[Borrowing]):
        """Send confirmation email for borrowed books"""
        if not borrowings:
            return

        user = borrowings[0].user
        context = {
            'user': user,
            'borrowings': borrowings
        }

        html_message = render_to_string(
            'emails/borrowing_confirmation.html',
            context
        )

        send_mail(
            subject='Book Borrowing Confirmation',
            message='',
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

    @staticmethod
    def send_return_reminder(borrowing: Borrowing):
        """Send reminder email for books due soon"""
        days_remaining = (borrowing.due_date - timezone.now()).days
        if days_remaining < 0 or days_remaining > 3:
            return

        context = {
            'user': borrowing.user,
            'borrowings': [borrowing],
            'days_remaining': days_remaining
        }

        html_message = render_to_string(
            'emails/return_reminder.html',
            context
        )

        send_mail(
            subject='Book Return Reminder',
            message='',
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[borrowing.user.email],
            fail_silently=False
        )

    @staticmethod
    def notify_book_available(book):
        """Send WebSocket notification when a book becomes available"""
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'book_availability',
            {
                'type': 'book.available',
                'book_id': book.id,
                'title': book.title,
                'message': f'Book "{book.title}" is now available'
            }
        ) 
