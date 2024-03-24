from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from .models import *


class Attachment(APIView):
    serializer_class = AttachmentCreateSerializer
    querysets = Attachment.objects.all()
    
    
    def post(self, request):
        data = request.data
        serial_data = self.serializer_class(data=data)
        if serial_data.is_valid():
            serial_data.save()
            return Response({"data": serial_data.data}, status=status.HTTP_201_CREATED)
        
        return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        data_counter = self.querysets.count()
        para = request.query_params.dict()
        if para.get("object_id"):
            querysets = self.querysets.filter(id=para.get("object_id"))
            attachment = AttachmentCreateSerializer(querysets ,many = True )
            return Response(
                {"data": attachment.data, "total_count": data_counter},
                status= status.HTTP_200_OK,
            )
        if para.get("content_type"):
            querysets = self.querysets.filter(contains = para.get("content_type"))
            attachment = AttachmentCreateSerializer(querysets, many = True)
            return Response(
                {"data":attachment.data, "total_count": data_counter},
                status = status.HTTP_200_OK,
            )
        attachment = AttachmentCreateSerializer(self.querysets ,many= True )
        return Response(
            {"data": attachment.data, "total_count": data_counter}, status=status.HTTP_200_OK
        )        