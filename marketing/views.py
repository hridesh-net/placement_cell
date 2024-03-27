from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *

# class Marketing(APIView):
#     serializer_class = OrganisationCreateSerializer
#     querysets = Organisation.objects.all()
    
    
#     def post(self, request):
#         try:
#             data = request.data
#             serial_data = self.serializer_class(data=data)
#             if serial_data.is_valid():
#                 serial_data.save()
#                 return Response({"data": serial_data.data}, status= status.HTTP_201_CREATED)
            
#             return Response({"message": "invaid data"}, status= status.HTTP_400_BAD_REQUEST
#         except:
#             return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)                
                