import random
import smtplib
import datetime
from django.conf import settings
from django.utils import timezone
from django.core import serializers
from django.db import IntegrityError
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from .models import Organisation, Job
from .serializers import OrganisationCreateSerializer, OrganisationGetSerializer, JobCreateSerializer, JobGetSerializer

class OrganisationView(generics.CreateAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationCreateSerializer

    def perform_create(self, serializer):
        organization = serializer.save()
        otp = ''.join(random.choices('0123456789', k=6))
        otp_created_at = timezone.now()
        self.request.session['organization_id'] = organization.id
        self.request.session['otp'] = otp
        self.request.session['otp_created_at'] = otp_created_at.isoformat()
        send_otp_email(organization.email, otp)
    def create(self, request, *args, **kwargs):
        data = request.data
        # Check for verification success message
        success_message = request.session.pop('verification_success', None)
        # Check for duplicate email
        if Organisation.objects.filter(email=data.get('email')).exists():
            return Response({"email": ["Organization with this email already exists."]}, status=status.HTTP_400_BAD_REQUEST)
        # Check for required fields
        required_fields = ['name', 'contact_details', 'industry_type', 'location', 'email', 'created_by']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return Response({field: ["This field is required."] for field in missing_fields}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return redirect('verify-otp')
        response_data = serializer.errors
        if success_message:
            response_data['message'] = success_message

        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        organizations = self.get_queryset()
        serializer = OrganisationGetSerializer(organizations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
def send_otp_email(to_email, otp):
    subject = 'Your OTP Code'
    message_body = f'Your OTP code is {otp}'
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        message = f'Subject: {subject}\n\n{message_body}'
        server.sendmail(settings.EMAIL_HOST_USER, to_email, message)
        server.quit()
        return True
    except IntegrityError:
        raise serializers.ValidationError({"created_by": ["An organization with this creator already exists."]})

class VerifyOTPView(APIView):
    def get(self, request, *args, **kwargs):
        organization_id = request.session.get('organization_id')
        if organization_id:
            try:
                organization = Organisation.objects.get(id=organization_id)
                return render(request, 'verify_otp.html', {'email': organization.email})
            except Organisation.DoesNotExist:
                return Response({'message': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Session data not found'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')
        organization_id = request.session.get('organization_id')
        stored_otp = request.session.get('otp')
        otp_created_at = request.session.get('otp_created_at')
        # Debug prints
        print(f"Email: {email}")
        print(f"Entered OTP: {otp}")
        print(f"Stored OTP: {stored_otp}")
        print(f"OTP Created At: {otp_created_at}")
        print(f"Current Time: {timezone.now()}")
        if not (email and otp and organization_id and stored_otp):
            return Response({'message': 'Missing required parameters'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            organization = Organisation.objects.get(id=organization_id, email=email)
            if otp == stored_otp:
                # Check if OTP is within valid time (10 minutes)
                if otp_created_at:
                    otp_created_at = datetime.datetime.fromisoformat(otp_created_at)
                    if (timezone.now() - otp_created_at) < datetime.timedelta(minutes=10):
                        organization.email_verified = True
                        organization.save()
                        # Set success message in session
                        request.session['verification_success'] = 'Email verified successfully'
                        return redirect('create-organisation')
                    else:
                        return Response({'message': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': 'OTP creation time not found'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except Organisation.DoesNotExist:
            return Response({'message': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

class JobView(APIView):
    serializer_class = JobCreateSerializer
    queryset = Job.objects.all()
    def post(self, request):
        data = request.data
        serial_data = self.serializer_class(data=data)
        if serial_data.is_valid():
            serial_data.save()
            return Response({"data": serial_data.data}, status=status.HTTP_201_CREATED)
    
        return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        data_count = self.queryset.count()
        params = request.query_params.dict()
    
        if params.get("id"):
            querysets = self.queryset.filter(id=params.get("id"))
            jobs = JobGetSerializer(querysets, many=True).data
            return Response(
                {"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK
            )
    
        if params.get("title"):
            querysets = self.queryset.filter(title__icontains(params.get("title")))
            jobs = JobGetSerializer(querysets, many=True).data
            return Response(
                {"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK
            )
    
        if params.get("organisation"):
            querysets = self.queryset.filter(company=params.get("organisation"))
            jobs = JobGetSerializer(querysets, many=True).data
            return Response(
                {"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK
            )
    
        if params.get("location"):
            querysets = self.queryset.filter(work_location=params.get("location"))
            jobs = JobGetSerializer(querysets, many=True).data
            return Response(
                {"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK
            )

        jobs = JobGetSerializer(self.queryset, many=True).data
        return Response(
            {"data": jobs, "total_count": data_count}, status=status.HTTP_200_OK
        )
