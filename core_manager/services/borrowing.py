from django.db import transaction
from django.utils import timezone
from typing import List, Tuple

from core_manager.models.borrowing import Borrowing
from ..models import Book, User
from .notification import NotificationService
from ..tasks import send_borrowing_confirmation

class BorrowingService:
    MAX_ACTIVE_BORROWINGS = 3
    DEFAULT_MAX_BORROWING_DAYS = 30

    @staticmethod
    @transaction.atomic
    def create_borrowing(user: User, book: Book, days: int = DEFAULT_MAX_BORROWING_DAYS):
        """
        Create a new borrowing record.
        Args:
            user: User instance
            book: Book instance
            days: Number of days to borrow
        Returns:
            Borrowing instance
        Raises:
            ValueError: If borrowing rules are violated
        """
        # Check if user has reached borrowing limit
        active_borrowings = Borrowing.objects.filter(
            user=user,
            status__in=['pending', 'active']
        ).count()

        if days > BorrowingService.DEFAULT_MAX_BORROWING_DAYS:
            raise ValueError(f"Maximum borrowing days is {BorrowingService.DEFAULT_MAX_BORROWING_DAYS} days")
        
        if active_borrowings >= BorrowingService.MAX_ACTIVE_BORROWINGS:
            raise ValueError("User has reached maximum number of active borrowings")

        # Check if book is available
        if not book.is_available():
            raise ValueError("Book is not available for borrowing")

        # Create borrowing record
        borrowing = Borrowing.objects.create(
            user=user,
            book=book,
            due_date=timezone.now() + timezone.timedelta(days=days),
            status='pending'
        )

        # Update book availability
        book.available_copies -= 1
        book.save()

        return borrowing

    @staticmethod
    @transaction.atomic
    def return_book(borrowing: Borrowing):
        """
        Return a borrowed book.
        Args:
            borrowing: Borrowing instance
        Returns:
            Updated Borrowing instance
        Raises:
            ValueError: If book is already returned
        """
        if borrowing.status in ['returned', 'cancelled']:
            raise ValueError("Book is already returned or borrowing was cancelled")

        # Update borrowing record
        borrowing.returned_date = timezone.now()
        borrowing.status = 'returned'
        borrowing.fine_amount = borrowing.calculate_fine()
        borrowing.save()

        # Update book availability
        book = borrowing.book
        book.available_copies += 1
        book.save()

        return borrowing

    @staticmethod
    def get_user_borrowings(user: User, status=None):
        """
        Get all borrowings for a user.
        Args:
            user: User instance
            status: Optional status filter
        Returns:
            QuerySet of borrowings
        """
        queryset = Borrowing.objects.filter(user=user)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    @staticmethod
    def check_overdue_borrowings():
        """
        Check and update status of overdue borrowings.
        Returns:
            Number of updated borrowings
        """
        overdue_borrowings = Borrowing.objects.filter(
            status='active',
            due_date__lt=timezone.now()
        )
        
        count = overdue_borrowings.count()
        overdue_borrowings.update(status='overdue')
        
        return count 

    @staticmethod
    @transaction.atomic
    def create_bulk_borrowings(user: User, books: List[Book], days: int = DEFAULT_MAX_BORROWING_DAYS) -> List[Borrowing]:
        """
        Create multiple borrowing records in a single transaction.
        Args:
            user: User instance
            books: List of Book instances
            days: Number of days to borrow
        Returns:
            List of created Borrowing instances
        Raises:
            ValueError: If borrowing rules are violated
        """
        if not books:
            raise ValueError("No books provided for borrowing")

        # Check if user has reached borrowing limit
        active_borrowings = Borrowing.objects.filter(
            user=user,
            status__in=['pending', 'active']
        ).count()

        if active_borrowings + len(books) > BorrowingService.MAX_ACTIVE_BORROWINGS:
            raise ValueError(f"User can only have {BorrowingService.MAX_ACTIVE_BORROWINGS} active borrowings")

        if days > BorrowingService.DEFAULT_MAX_BORROWING_DAYS:
            raise ValueError(f"Maximum borrowing days is {BorrowingService.DEFAULT_MAX_BORROWING_DAYS} days")

        # Check if all books are available
        unavailable_books = [book for book in books if not book.is_available()]
        if unavailable_books:
            raise ValueError(f"Books not available: {', '.join(book.title for book in unavailable_books)}")

        # Create borrowing records
        borrowings = []
        for book in books:
            borrowing = Borrowing(
                user=user,
                book=book,
                due_date=timezone.now() + timezone.timedelta(days=days),
                status='pending'
            )
            borrowings.append(borrowing)

            # Update book availability
            book.available_copies -= 1
            book.save()

        # Save borrowings
        Borrowing.objects.bulk_create(borrowings)

        # Send confirmation email asynchronously
        send_borrowing_confirmation.delay([b.id for b in borrowings])

        return borrowings

    @staticmethod
    @transaction.atomic
    def return_bulk_books(borrowings: List[Borrowing]) -> List[Borrowing]:
        """
        Return multiple borrowed books in a single transaction.
        Args:
            borrowings: List of Borrowing instances
        Returns:
            List of updated Borrowing instances
        Raises:
            ValueError: If any book is already returned
        """
        if not borrowings:
            raise ValueError("No borrowings provided for return")

        # Check if any borrowing is already returned
        already_returned = [b for b in borrowings if b.status in ['returned', 'cancelled']]
        if already_returned:
            raise ValueError(f"Books already returned: {', '.join(str(b) for b in already_returned)}")

        # Update borrowing records
        updated_borrowings = []
        for borrowing in borrowings:
            borrowing.returned_date = timezone.now()
            borrowing.status = 'returned'
            borrowing.fine_amount = borrowing.calculate_fine()
            borrowing.save()

            # Update book availability
            book = borrowing.book
            book.available_copies += 1
            book.save()

            # Notify that book is available
            NotificationService.notify_book_available(book)

            updated_borrowings.append(borrowing)

        return updated_borrowings 
