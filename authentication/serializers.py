from .models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name","last_name","role","username","password"]
        extra_kwargs = {"password":{"write_only":True}}


    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        if username is None:
            raise ValueError("Username must be required.")
        if password is None:
            raise ValueError("Password must be required")
        return attrs

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return User.objects.create(**validated_data)
    


    
    