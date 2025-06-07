from core_manager.filters.book_filters import BookFilter
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from ..models import Book
from ..serializers.book import BookSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'isbn', 'description', 'publisher']
    ordering_fields = ['title', 'created_at']
    filterset_class = BookFilter
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('author', 'category')
        return queryset
