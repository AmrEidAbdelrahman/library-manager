from django_filters import rest_framework as filters
from ..models import Book

class BookFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__slug', lookup_expr='icontains')
    author = filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    library = filters.CharFilter(field_name='library__name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'isbn': ['exact'],
            'description': ['icontains'],
        }
