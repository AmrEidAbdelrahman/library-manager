from core_manager.models.book import Book
from core_manager.models.borrowing import Borrowing
from core_manager.serializers.user_serializers import UserSerializer
from rest_framework import serializers
from .book import BookSerializer
from django.utils import timezone

class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True, fields=['id', 'title', 'isbn', 'author_name', 'category_name', 'category'])
    user = UserSerializer(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    penalty_amount = serializers.SerializerMethodField()

    def get_penalty_amount(self, obj):
        """Calculate penalty amount based on overdue days"""
        return obj.calculate_fine()

    class Meta:
        model = Borrowing
        fields = [
            'id', 'book', 'user', 'borrowed_date', 'due_date',
            'returned_date', 'status', 'notes',
            'is_overdue', 'created_at', 'updated_at', 'penalty_amount'
        ]
        read_only_fields = [
            'id', 'borrowed_date', 'returned_date', 'status', 'created_at', 'updated_at'
        ]


class BorrowingCreateSerializer(serializers.Serializer):
    book_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    days = serializers.IntegerField(write_only=True, min_value=1, max_value=30)

    def validate_book_ids(self, value):
        """Validate that the book is available for borrowing"""
        books = Book.objects.filter(id__in=value, available_copies__gt=0)
        if len(books) != len(value):
            return serializers.ValidationError({
                "book_ids": "Some books do not exist or are not available for borrowing."
            })
        
        # allow up to 3 books to be borrowed for a single user
        user = self.context['request'].user
        if Borrowing.objects.filter(user=user, status='active').count() + len(value) >= 3:
            raise serializers.ValidationError({
                "book_ids": "You cannot borrow more than 3 books."
            })
        
        return value
    
class BorrowingBulkReturnSerializer(serializers.Serializer):
    borrowing_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )

    def validate_borrowing_ids(self, value):
        """Validate that borrowings exist and belong to the user"""
        user = self.context['request'].user
        borrowings = Borrowing.objects.filter(id__in=value, user=user)
        if len(borrowings) != len(value):
            raise serializers.ValidationError({
                "borrowing_ids": "Some borrowings do not exist or do not belong to you."
            })
        return value
