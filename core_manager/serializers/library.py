from rest_framework import serializers
from ..models import Library
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D, Distance

class LibrarySerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    def get_distance(self, obj):
        if hasattr(obj, 'distance'):
            return round(obj.distance.km, 2)
        return None
            
    class Meta:
        model = Library
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_location(self, value):
        if not value:
            raise serializers.ValidationError("Location is required")
        return value 
