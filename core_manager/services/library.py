from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from ..models import Library

class LibraryService:
    @staticmethod
    def get_nearby_libraries(lat: float, lng: float, radius: float = 10.0):
        """
        Find libraries within a specified radius of given coordinates.
        Args:
            lat: Latitude
            lng: Longitude
            radius: Radius in kilometers
        Returns:
            QuerySet of nearby libraries ordered by distance
        """
        point = Point(lng, lat, srid=4326)
        return Library.objects.filter(
            location__distance_lte=(point, D(km=radius))
        ).distance(point).order_by('distance')

    @staticmethod
    def is_library_open(library: Library, timestamp=None):
        """
        Check if a library is open at the given timestamp.
        Args:
            library: Library instance
            timestamp: datetime object (defaults to now)
        Returns:
            bool: True if library is open, False otherwise
        """
        from datetime import datetime
        if timestamp is None:
            timestamp = datetime.now()

        day_of_week = timestamp.strftime('%A').lower()
        hours = library.opening_hours.get(day_of_week, {})
        
        if not hours:
            return False

        current_time = timestamp.strftime('%H:%M')
        return hours.get('open', '00:00') <= current_time <= hours.get('close', '23:59') 
