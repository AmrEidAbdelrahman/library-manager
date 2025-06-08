from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils import timezone
from .book import Book
from .user import User

class Borrowing(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('active', _('Active')),
        ('returned', _('Returned')),
        ('overdue', _('Overdue')),
        ('cancelled', _('Cancelled')),
    ]

    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='borrowings')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='borrowings')
    borrowed_date = models.DateTimeField(_('borrowed date'), default=timezone.now)
    due_date = models.DateTimeField(_('due date'))
    returned_date = models.DateTimeField(_('returned date'), null=True, blank=True)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('borrowing')
        verbose_name_plural = _('borrowings')
        ordering = ['-borrowed_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.book.title}"

    def calculate_fine(self):
        """Calculate fine amount based on overdue days"""
        if self.status in ['returned', 'overdue'] and self.returned_date:
            days_overdue = (self.returned_date - self.due_date).days
            if days_overdue > 0:
                # Example: $1 per day overdue
                return days_overdue * 1.00
        return 0

    def is_overdue(self):
        """Check if the borrowing is overdue"""
        return timezone.now() > self.due_date and self.status == 'active'

    def can_be_renewed(self):
        """Check if the borrowing can be renewed"""
        return (
            self.status == 'active' and
            not self.is_overdue() and
            self.book.is_available()
        )

    def renew(self, days=14):
        """Renew the borrowing for additional days"""
        if not self.can_be_renewed():
            raise ValueError("This borrowing cannot be renewed")
        
        self.due_date = self.due_date + timezone.timedelta(days=days)
        self.save()
        return True 
