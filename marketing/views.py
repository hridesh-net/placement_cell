from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from utils.mail import organization_registration_email, job_posted_email
from utils.pagination import SpecificPagination

# Create your views here.

class OrganisationView(APIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationCreateSerializer

    def get(self, request):
        params = request.query_params.dict()
        data_count = self.queryset.count()

        if params.get("id"):
            queryset = self.queryset.filter(id=params.get("id"))
            org = OrganisationGetSerializer(queryset, many=True).data
            return Response(
                {"data": org, "total_count": data_count}, status=status.HTTP_200_OK
            )

        if params.get("name"):
            queryset = self.queryset.filter(name__icontains=params.get("name"))
            org = OrganisationGetSerializer(queryset, many=True).data
            return Response(
                {"data": org, "total_count": data_count}, status=status.HTTP_200_OK
            )

        org = OrganisationGetSerializer(self.queryset, many=True).data
        return Response(
            {"data": org, "total_count": data_count}, status=status.HTTP_200_OK
        )

    def post(self, request):
        data = request.data
        serial_data = self.serializer_class(data=data)
        if serial_data.is_valid():
            instance = serial_data.save()
            # organization registered mail
            if instance.created_by:
                organization_registration_email(instance.name, instance.created_by.email)
            return Response({"data": serial_data.data}, status=status.HTTP_201_CREATED)

        return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class JobView(APIView):
    serializer_class = JobCreateSerializer
    queryset = Job.objects.all()
    pagination_class = SpecificPagination()

    def post(self, request):
        data = request.data
        serial_data = self.serializer_class(data=data)
        if serial_data.is_valid():
            instance = serial_data.save()
            instance_data = JobGetSerializer(instance).data
            if instance.company and instance.company.created_by:
                job_posted_email(instance_data, instance.company.created_by.email)
            return Response({"data": serial_data.data}, status=status.HTTP_201_CREATED)

        return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = self.queryset
        params = request.query_params

        if 'id' in params:
            queryset = queryset.filter(id=params.get('id'))

        if 'title' in params:
            queryset = queryset.filter(title__icontains=params.get('title'))

        if 'company' in params:
            queryset = queryset.filter(company=params.get('company'))

        if 'work_location' in params:
            queryset = queryset.filter(work_location=params.get('work_location'))

        if 'location' in params:
            queryset = queryset.filter(company__location__icontains=params.get('location'))

        paginated_response = self.pagination_class.pagination_models(request, queryset, params, JobGetSerializer)
        if paginated_response is not None:
            return paginated_response

        jobs = JobGetSerializer(queryset, many=True).data
        return Response(
            {"data": jobs, "total_count": queryset.count()}, status=status.HTTP_200_OK
        )