from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *

class ApplicantView(APIView):
    serializer_class = ApplicantCreatSerializer
    querysets = Applicant.objects.all()

    def post(self, request):
        data = request.data
        serial_data = self.serializer_class(data=data)
        if serial_data.is_valid():
            serial_data.save()
            return Response({"data": serial_data.data}, status=status.HTTP_201_CREATED)

        return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        data_count = self.querysets.count()
        params = request.query_params.dict()
        if params.get("id"):
            querysets = self.querysets.filter(id=params.get("id"))
            applicants = ApplicantCreatSerializer(querysets, many=True)
            return Response(
                {"data": applicants.data, "total_count": data_count},
                status=status.HTTP_200_OK,
            )
        if params.get("name"):
            querysets = self.querysets.filter(name__contains=params.get("name"))
            applicants = ApplicantCreatSerializer(querysets, many=True)
            return Response(
                {"data": applicants.data, "total_count": data_count},
                status=status.HTTP_200_OK,
            )
        applicants = ApplicantCreatSerializer(self.querysets, many=True)
        return Response(
            {"data": applicants.data, "total_count": data_count}, status=status.HTTP_200_OK
        )

class ApplicantProfileView(APIView):
    serializer_class =ApplicantProfileCreateSeializer
    querysets = ApplicantProfile.objects.all()
    
    
    def post(self, request):
        data = request.data
        serial_data = self.serializer_class(data=data)
        if serial_data.is_valid():
            serial_data.save()
            return Response({"data": serial_data.data}, status=status.HTTP_201_CREATED)

        return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        data_count = self.querysets.count()
        params = request.query_params.dict()
        if params.get("id"):
            querysets = self.querysets.filter(id=params.get("id"))
            applicants = self.serializer_class(querysets, many=True)
            return Response(
                {"data": applicants.data, "total_count": data_count},
                status=status.HTTP_200_OK,
            )
        if params.get("name"):
            querysets = self.querysets.filter(name__contains=params.get("name"))
            applicants = self.serializer_class(querysets, many=True)
            return Response(
                {"data": applicants.data, "total_count": data_count},
                status=status.HTTP_200_OK,
            )
        applicants = self.serializer_class(self.querysets, many=True)
        return Response(
            {"data": applicants.data, "total_count": data_count}, status=status.HTTP_200_OK
        )
        

class ApplicationView(APIView):
    serializer_class = ApplicationCreateSerializer
    querysets = Application.objects.all()

    #############Application post api##################
    def post(self, request):
        data = request.data
        serial_data = self.serializer_class(data=data)
        if serial_data.is_valid():
            serial_data.save()
            return Response({"data": serial_data.data}, status=status.HTTP_201_CREATED)
        else:
            print(serial_data.errors)

        return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    ########### application get api##############
    def get(self, request):
        data_count = self.querysets.count()
        student = request.query_params.get("student",None)
        applicant_profile = request.query_params.get("applicant_profile",None)
        if student: 
            querysets = self.querysets.filter(student =student)
            application= ApplicationCreateSerializer(querysets, many= True)
            return Response(
                {"data": application.data, "total_count": data_count},
                status=status.HTTP_200_OK,
            )
            
        if applicant_profile: 
            querysets = self.querysets.filter(applicant_profile = applicant_profile ) 
            application= ApplicationCreateSerializer(querysets, many= True)
            return Response(
                {"data": application.data, "total_count": data_count},
                status=status.HTTP_200_OK,
            ) 
        application= ApplicationCreateSerializer(self.querysets, many= True)    
        return Response(
                {"data": application.data, "total_count": data_count},
                status=status.HTTP_200_OK,
            )    
    
            
        