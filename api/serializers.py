from rest_framework import serializers
from .models import User, FriendRequest
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        # Override to validate email instead of username
        self.user = User.objects.filter(email=attrs[self.username_field]).first()

        if self.user is None:
            raise serializers.ValidationError("No user with this email")

        # Check password
        if not self.user.check_password(attrs['password']):
            raise serializers.ValidationError("Incorrect password")

        data = super().validate(attrs)

        # Custom token fields
        data.update({'email': self.user.email})
        
        # Update the last login time for the user
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data