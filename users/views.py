from django.shortcuts import render
from .serializers import UserSerializer,ProfileSerializer
from .models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .permission import IsLibrarian
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Profile

# Create your views here.

@api_view(["GET"])
@permission_classes([IsLibrarian])
def get_all_user(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)
    return Response({"users":serializer.data
                    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    try:
        user = request.user
        if user.role == "Librarian":
            user_profile = request.user.profile
        if user.role == "Student":
            user_profile = request.user.profile
        else:
            user_profile = request.user.profile
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)

    serializer = ProfileSerializer(user_profile)

    return Response({"profile": serializer.data})
