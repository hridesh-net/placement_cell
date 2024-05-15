from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from .serializers import UserLoginSerializer
from .models import CustomUser

# Create your views here.


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({'error': "email required"}, status=status.HTTP_400_BAD_REQUEST)

        usr = CustomUser.objects.filter(email=email).first()
        if not usr:
            return Response({'error': "No user with following email"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = authenticate(email=usr.email, password=request.data.get("password").strip())
            if user:
                user.last_login = timezone.now()
                user.save()

                # Serialize user data
                serializer = UserLoginSerializer(user)
                response_data = serializer.data
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)