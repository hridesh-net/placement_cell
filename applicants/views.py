from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import *
from .serializers import *


class ApplicantView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

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
            {"data": applicants.data, "total_count": data_count},
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        data = request.data
        id = request.query_params.get("id")
        applicant = Applicant.objects.get(id=id)
        serial_data = self.serializer_class(applicant, data=data, partial=True)
        if serial_data.is_valid():
            serial_data.save()
            return Response({"data": serial_data.data}, status=status.HTTP_201_CREATED)

        return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class ApplicantProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    serializer_class = ApplicantProfileCreateSeializer
    get_serializer_class = ApplicantProfileGetSerializer
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
        applicants = self.get_serializer_class(self.querysets, many=True)
        return Response(
            {"data": applicants.data, "total_count": data_count},
            status=status.HTTP_200_OK,
        )

    def put(self, request):
        data = request.data
        id = request.query_params.get("applicantId")
        applicant_profile = ApplicantProfile.objects.get(applicant=id)

        for key, value in data.items():
            if hasattr(applicant_profile, key):
                setattr(applicant_profile, key, value)
            else:
                return Response(
                    {"message": f"Invalid field: {key}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            applicant_profile.save()
            serial_data = self.get_serializer_class(applicant_profile)
            return Response({"data": serial_data.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ApplicationView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    serializer_class = ApplicationCreateSerializer
    querysets = Application.objects.all()

    #############Application post api##################
    def post(self, request):
        data = request.data
        dup_application = self.querysets.filter(
            aplicant=data.get("applicant"),
            applicant_profile=data.get("applicant_profile"),
            job=data.get("job"),
        )
        if dup_application:
            return Response(
                {"message": "Application already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
        applicant = request.query_params.get("applicant", None)
        applicant_profile = request.query_params.get("applicant_profile", None)
        if applicant:
            querysets = self.querysets.filter(applicant=applicant)
            application = ApplicationCreateSerializer(querysets, many=True)
            return Response(
                {"data": application.data, "total_count": data_count},
                status=status.HTTP_200_OK,
            )

        if applicant_profile:
            querysets = self.querysets.filter(applicant_profile=applicant_profile)
            application = ApplicationCreateSerializer(querysets, many=True)
            return Response(
                {"data": application.data, "total_count": data_count},
                status=status.HTTP_200_OK,
            )
        application = ApplicationCreateSerializer(self.querysets, many=True)
        return Response(
            {"data": application.data, "total_count": data_count},
            status=status.HTTP_200_OK,
        )
