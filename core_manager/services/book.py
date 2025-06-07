from django.db import transaction
from ..models import Book

class BookService:
    @staticmethod
    @transaction.atomic
    def borrow_book(book: Book):
        """
        Borrow a book if available.
        Args:
            book: Book instance
        Returns:
            bool: True if book was borrowed successfully
        Raises:
            ValueError: If book is not available
        """
        if not book.is_available():
            raise ValueError("Book is not available for borrowing")
        
        book.available_copies -= 1
        book.save()
        return True

    @staticmethod
    @transaction.atomic
    def return_book(book: Book):
        """
        Return a book.
        Args:
            book: Book instance
        Returns:
            bool: True if book was returned successfully
        Raises:
            ValueError: If all copies are already available
        """
        if book.available_copies >= book.total_copies:
            raise ValueError("All copies of this book are already available")
        
        book.available_copies += 1
        book.save()
        return True

    @staticmethod
    def get_available_books(library=None):
        """
        Get all available books, optionally filtered by library.
        Args:
            library: Optional Library instance
        Returns:
            QuerySet of available books
        """
        queryset = Book.objects.filter(available_copies__gt=0)
        if library:
            queryset = queryset.filter(library=library)
        return queryset 
