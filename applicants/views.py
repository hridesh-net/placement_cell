from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Applicant
from .serializers import ApplicantCreatSerializer

# Create your views here.


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
        print(params)
        if params.get("id"):
            print("yes")
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
