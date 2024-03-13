
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError as DRFValidationError
from .models import saved_password


User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']

    def validate(self, data):
        password = data.get('password')
        try:
            validate_password(password)
        except DRFValidationError as e:
            raise serializers.ValidationError({'password': e.detail})

        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']

class ViewPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = saved_password
        fields = ['id', 'account_type', 'password']