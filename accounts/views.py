from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from .models import CustomUser
from .serializers import UserLoginSerializer, UserSignupSerializer

# Create your views here.


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "email required"}, status=status.HTTP_400_BAD_REQUEST
            )

        usr = CustomUser.objects.filter(email=email).first()
        if not usr:
            return Response(
                {"error": "No user with following email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = authenticate(
                email=usr.email, password=request.data.get("password").strip()
            )
            if user:
                user.last_login = timezone.now()
                user.save()

                # Serialize user data
                serializer = UserLoginSerializer(user)
                response_data = serializer.data
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignupAPIView(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(
                    {"message": "User created successfully"},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
