from django.shortcuts import render
from . serializers import RegistrationSerializer
from rest_framework import request,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

class Register(APIView):
    def post(self,request,*args,**kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if request.data.get("role") == "Librarian":
                serializer.save(is_staff=True)
            else:
                serializer.save()
            return Response({"message":"Register successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors})
        
class Login(APIView):
    def post(self,request,*args,**kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request,username=username,password=password)

        if user is not None:

            token = TokenObtainPairSerializer(data=request.data)
            token.is_valid(raise_exception=True)
            tokens = token.validated_data

            if user.role == "Student":
                return Response({"message":"Student login successfully...","token":{"access_token":str(tokens["access"]),"refresh_token":str(tokens["refresh"])}})
            if user.role == "Librarian":
                return Response({"message":"Librarian login successfully...","token":{"access_token":str(tokens["access"]),"refresh_token":str(tokens["refresh"])}})
            else:
                return Response({"message":"Admin register successfully...","token":{"access_token":str(tokens["access"]),"refresh_token":str(tokens["refresh"])}})
        else:
            raise ValidationError("Invalid username and password")
