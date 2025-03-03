from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import UserProfile
from rest_framework.exceptions import ValidationError

class BaseUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

class RegisterSerializer(BaseUserSerializer):
    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username

class AuthSerializer(BaseUserSerializer):
    pass

class ConfirmUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise ValidationError({"username": "User does not exist"})


        return data

    def confirm_user(self):
        user = User.objects.get(username=self.validated_data['username'])
        user.is_active = True
        user.userprofile.confirmation_code = None
        user.save()

        return user
