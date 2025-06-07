from core_manager.serializers.book import BookSerializer
from library_management.serializers import DynamicFieldsMixinSerializer
from rest_framework import serializers
from ..models import Author

class AuthorSerializer(DynamicFieldsMixinSerializer, serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True, fields=['id', 'title', 'isbn', 'author_name', 'category_name', 'category'])
    book_count = serializers.SerializerMethodField()

    def get_book_count(self, obj):
        if hasattr(obj, 'book_count'):
            return obj.book_count
        return None
    
    class Meta:
        model = Author
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at'] 
