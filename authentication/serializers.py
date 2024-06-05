from .models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name","last_name","role","username","password"]
        extra_kwargs = {"password":{"write_only":True}}


    def validate(self, attrs):
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")
        username = attrs.get("username")
        password = attrs.get("password")
        if username is None:
            raise ValidationError("Username must be required.")
        if first_name is None:
            raise ValidationError("First name must be required.")
        if last_name is None:
            raise ValidationError("Last name must be required.")
        if password is None:
            raise ValidationError("Password must be required")
        return attrs

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return User.objects.create(**validated_data)
    


    
    