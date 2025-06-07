from core_manager.serializers.category import CategorySerializer
from library_management.serializers import DynamicFieldsMixinSerializer
from rest_framework import serializers
from ..models import Book

class BookSerializer(DynamicFieldsMixinSerializer, serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_available']

    def validate_isbn(self, value):
        if not value.isdigit() or len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be 10 or 13 digits")
        return value
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'category' in representation:
            representation['category'] = CategorySerializer(instance.category).data
        return representation

