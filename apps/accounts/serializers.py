from rest_framework import serializers as rest_framework_serializers
from rest_framework.authtoken.models import Token as AuthToken
from rest_framework import exceptions

from django.contrib.auth import authenticate
from django.db.models import F, fields

from apps.accounts import models as accounts_models


class UserSerializer(rest_framework_serializers.ModelSerializer):
    """
    Custom User Serializer class
    """
    token = rest_framework_serializers.SerializerMethodField()

    class Meta:
        model = accounts_models.User
        fields = ['mobile_number', 'name', 'password', 'token']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        user = accounts_models.User(
            name = validated_data['name'],
            mobile_number = validated_data['mobile_number'],
            password = validated_data['password'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_token(self, user):
        """
        Creating token for already registered user
        """
        return AuthToken.objects.create(user = user).key


class LoginSerializer(rest_framework_serializers.Serializer):
    """
    Validating login credentials
    """
    mobile_number = rest_framework_serializers.CharField()
    password = rest_framework_serializers.CharField()

    def validate(self, attrs):
        """
        Validating if user exists with given credentials
        """
        mobile_number = attrs.get('mobile_number')
        password = attrs.get('password')
        user = authenticate(mobile_number=mobile_number, password=password)
        if not user:
            raise exceptions.ValidationError('Unable to log in with provided credentials.')
        attrs['user'] = user
        return attrs


class UserProfileSerializer(rest_framework_serializers.ModelSerializer):
    """
    User Profile Serializer
    """

    class Meta:
        model = accounts_models.User
        fields = '__all__'
