from rest_framework import serializers
from django.contrib.auth.hashers import make_password

# Model for API
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'telephone', 'group')
        extra_kwargs = {'password': {'write_only': True}}