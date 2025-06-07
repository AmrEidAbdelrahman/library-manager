from core_manager.filters.author_filters import AuthorFilter
from core_manager.models.book import Book
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..models import Author
from ..serializers.author import AuthorSerializer
from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch


class AuthorView(ModelViewSet):
    """
    AuthorView is a view for managing authors.
    It inherits from ModelViewSet and provides CRUD operations for authors.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    filterset_class = AuthorFilter

    def get_queryset(self):
        """
        Override the default queryset to order authors by book count.
        """
        if self.action == 'list_authors_with_books':
            books_with_category = Prefetch(
                'books',
                queryset=Book.objects.select_related('category')
            )
            return self.queryset.prefetch_related(books_with_category)
        return self.queryset.annotate(
            book_count=Count('books')
        ).order_by('-book_count', 'name')
    
    def get_serializer(self, *args, **kwargs):
        """
        Override the get_serializer method to include book count in the serializer context.
        """
        if self.action == 'list_authors_with_books':
            kwargs['fields'] = ['id', 'name', 'books']
        else:
            kwargs['exclude'] = ['books']
        return super().get_serializer(*args, **kwargs)

    @action(detail=False, methods=['get'], url_path='books')
    def list_authors_with_books(self, request):
        """
        Custom action to list authors with their book counts.
        This action returns a list of authors along with the count of books they have written.
        """
        authors = self.get_queryset()
        serializer = self.get_serializer(authors, many=True)
        return Response(serializer.data)

