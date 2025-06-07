from core_manager.models.author import Author
import django_filters as filters

class AuthorFilter(filters.FilterSet):
    """
    AuthorFilter is a filter class for filtering authors based on their name.
    It uses Django's FilterSet to provide filtering capabilities.
    """
    library = filters.CharFilter(field_name='books__library__name', lookup_expr='icontains')
    category = filters.CharFilter(field_name='books__category__slug', lookup_expr='icontains')

    class Meta:
        model = Author
        fields = {
            'name': ['exact', 'icontains'],
        }
