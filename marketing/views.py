from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from utils.mail import organization_registration_email, job_posted_email

class OrganisationView(APIView):
    querysets = Organisation.objects.all()
    serializer_class = OrganisationSerializer

    def get(self, request):
        params = request.query_params.dict()
        data_count = self.querysets.count()

        if params.get("id"):
            querysets = self.querysets.filter(id=params.get("id"))
            org = OrganisationSerializer(querysets, many=True).data
            return Response({"data": org, "total_count": data_count}, status=status.HTTP_200_OK)

        if params.get("name"):
            querysets = self.querysets.filter(
                name__icontains=params.get("name"))
            org = OrganisationSerializer(querysets, many=True).data
            return Response({"data": org, "total_count": data_count}, status=status.HTTP_200_OK)

        org = OrganisationSerializer(self.querysets, many=True).data
        return Response({"data": org, "total_count": data_count}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serial_data = self.serializer_class(data=data)
        if serial_data.is_valid():
            instance=serial_data.save()
            # organization registered mail
            if instance.created_by:
                organization_registration_email(instance.name, instance.created_by.email)
            return Response({"data": serial_data.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "invalid data", "errors": serial_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class JobView(APIView):
    serializer_class = JobCreateSerializer
    querysets = Job.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        data = request.data.copy()
        files = request.FILES.getlist('attachments')
        data.setlist('attachments', files)

        serial_data = self.serializer_class(data=data)
        if serial_data.is_valid():
            instance=serial_data.save()
            #  job post mail
            instance_data = JobGetSerializer(instance).data
            if instance.company and instance.company.created_by:
                job_posted_email(instance_data, instance.company.created_by.email)
            return Response({"data": serial_data.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "invalid data", "errors": serial_data.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        data_count = self.querysets.count()
        params = request.query_params.dict()

        if params.get("id"):
            querysets = self.querysets.filter(id=params.get("id"))
            jobs = JobGetSerializer(querysets, many=True).data
            return Response({"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK)

        if params.get("title"):
            querysets = self.querysets.filter(
                title__icontains=params.get("title"))
            querysets = self.querysets.filter(title__icontains=params.get("title"))
            jobs = JobGetSerializer(querysets, many=True).data
            return Response(
                {"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK
            )
        
        ############# Changed this for company ############### 
        if params.get("company"):
            querysets = self.querysets.filter(company=params.get("company"))
            jobs = JobGetSerializer(querysets, many=True).data
            return Response({"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK)

        ############# Changed this for work location ############### 
        if params.get("work_location"):
            querysets = self.querysets.filter(work_location=params.get("work_location"))
            jobs = JobGetSerializer(querysets, many=True).data
            return Response({"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK)

          # Added more API 
    def delete(self, request):
        data = request.data
        job = Job.objects.get(id=data.get("id"))
        job.delete()
        return Response({"message": "Job deleted successfully"}, status=status.HTTP_200_OK)

    def put(self, request):
        data = request.data
        job = Job.objects.get(id=data.get("id"))
        serial_data = self.serializer_class(job, data=data)
        if serial_data.is_valid():
            serial_data.save()
            return Response({"data": serial_data.data}, status=status.HTTP_200_OK)
        return Response({"message": "invalid data", "errors": serial_data.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data = request.data
        job = Job.objects.get(id=data.get("id"))
        serial_data = self.serializer_class(job, data=data, partial=True)
        if serial_data.is_valid():
            serial_data.save()
            return Response({"data": serial_data.data}, status=status.HTTP_200_OK)
        return Response({"message": "invalid data", "errors": serial_data.errors}, status=status.HTTP_400_BAD_REQUEST)

      return Response(
          {"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK
      )
    