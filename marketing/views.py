from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

# Create your views here.


class OrganisationView(APIView):
    querysets = Organisation.objects.all()
    serializer_class = OrganisationCreateSerializer

    def get(self, request):
        params = request.query_params.dict()
        data_count = self.querysets.count()

        if params.get("id"):
            querysets = self.querysets.filter(id=params.get("id"))
            org = OrganisationGetSerializer(querysets, many=True).data
            return Response(
                {"data": org, "total_count": data_count}, status=status.HTTP_200_OK
            )

        if params.get("name"):
            querysets = self.querysets.filter(name__icontains=params.get("name"))
            org = OrganisationGetSerializer(querysets, many=True).data
            return Response(
                {"data": org, "total_count": data_count}, status=status.HTTP_200_OK
            )

        org = OrganisationGetSerializer(self.querysets, many=True).data
        return Response(
            {"data": org, "total_count": data_count}, status=status.HTTP_200_OK
        )

    def post(self, request):
        data = request.data
        serial_data = self.serializer_class(data=data)
        if serial_data.is_valid():
            serial_data.save()
            return Response({"data": serial_data.data}, status=status.HTTP_201_CREATED)

        return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class JobView(APIView):
    serializer_class = JobCreateSerializer
    querysets = Job.objects.all()

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
            jobs = JobGetSerializer(querysets, many=True).data
            return Response(
                {"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK
            )

        if params.get("title"):
            querysets = self.querysets.filter(title__icontains=params.get("name"))
            jobs = JobGetSerializer(querysets, many=True).data
            return Response(
                {"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK
            )

        if params.get("organisation"):
            querysets = self.querysets.filter(company=params.get("organisation"))
            jobs = JobGetSerializer(querysets, many=True).data
            return Response(
                {"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK
            )

        if params.get("location"):
            querysets = self.querysets.filter(work_location=params.get("location"))
            jobs = JobGetSerializer(querysets, many=True).data
            return Response(
                {"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK
            )

        jobs = JobGetSerializer(self.querysets, many=True).data
        return Response(
            {"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK
        )
