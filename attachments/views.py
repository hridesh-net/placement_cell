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
        try:
            data = request.data
            serial_data = self.serializer_class(data=data)
            if serial_data.is_valid():
                serial_data.save()
                return Response({"data": serial_data.data}, status=status.HTTP_201_CREATED)
            
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        data_counter = self.querysets.count()
        para = request.query_params.dict()
         
        content_type = request.query_params.get("content_type" , None)              
        object_id = request.query_params.get("object_id",None)
        content_object = request.query_params.get("content_objecyt", None)
        attachment_file = request.query_params.get("attachment_file", None)
        attachment_type = request.query_params.get("attachment_type", None)
        
        
        if object_id is not None:
            querysets = self.querysets.filter(object_id=object_id)
        if attachment_type is not None:
            querysets = self.querysets.filter(attachment_type = attachment_type)
            attachment = AttachmentCreateSerializer(querysets, many = True)
            return Response(
                {"data":attachment.data, "total_count": data_counter},
                status = status.HTTP_200_OK,
            )
        attachment = AttachmentCreateSerializer(self.querysets ,many= True )
        return Response(
            {"data": attachment.data, "total_count": data_counter}, status=status.HTTP_200_OK
        )
        