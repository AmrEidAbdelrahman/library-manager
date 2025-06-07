import django_filters as filters
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance


class LibraryFilter(filters.FilterSet):
    lat = filters.NumberFilter(method='filter_by_distance')
    lng = filters.NumberFilter(method='filter_by_distance')
    radius = filters.NumberFilter(method='filter_by_distance')

    book = filters.CharFilter(field_name='books__title', lookup_expr='icontains')
    category = filters.CharFilter(field_name='books__category__slug', lookup_expr='icontains')
    author = filters.CharFilter(field_name='books__author__name', lookup_expr='icontains')

    def filter_by_distance(self, queryset, field_name, value):
        # Filter by distance if coordinates are provided
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        radius = self.request.query_params.get('radius', 5000)

        if lat and lng:
            point = Point(float(lng), float(lat), srid=4326)
            queryset = queryset.annotate(
                distance=Distance('location', point)
            ).filter(
                distance__lte=D(km=float(radius))
            )
            queryset = queryset.order_by('distance')

        return queryset
