from core_manager.filters.library_filters import LibraryFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from ..models import Library
from ..serializers.library import LibrarySerializer
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.gis.db.models.functions import Distance


class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, filters.DjangoFilterBackend]
    search_fields = ['name', 'address', 'description', 'books__title', 'books__author__name']
    ordering_fieldswswww = ['created_at']
    filterset_class = LibraryFilter

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        if lat and lng:
            context['user_location'] = Point(float(lng), float(lat), srid=4326)
        return context
    
    def get_queryset(self):
        user = self.request.user
        user_location = getattr(user, 'location', None)

        if user.is_authenticated and user_location:
            # Make sure it's a GEOS Point with SRID 4326
            user_point = Point(user_location.x, user_location.y, srid=4326)

            return Library.objects.annotate(
                distance=Distance('location', user_point)
            ).order_by('distance')
        return Library.objects.all()
