

from rest_framework import serializers
from core_manager.models.user import User
from library_management.serializers import DynamicFieldsMixinSerializer


class UserSerializer(DynamicFieldsMixinSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']

    def validate_email(self, value):
        """Validate that email is unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email must be unique")
        return value

    def validate_username(self, value):
        """Validate that username is unique"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username must be unique")
        return value
