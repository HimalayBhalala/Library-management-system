from .models import Profile
from rest_framework import serializers
from authentication.models import User

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    is_staff = serializers.BooleanField(source="user.is_staff")
    is_active = serializers.BooleanField(source="user.is_active")
    is_superuser = serializers.BooleanField(source="user.is_superuser")
    role = serializers.CharField(source="user.role")
    date_joined = serializers.DateTimeField(source="user.date_joined")

    class Meta:
        model = Profile
        fields = ["id","username","first_name","last_name","is_staff","is_active","is_superuser","date_of_birth","role","date_joined"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","first_name","username","last_name","is_staff","is_superuser","role"]