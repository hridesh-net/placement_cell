from rest_framework import serializers
from .models import Organization, Job

class OrganizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ('id','email_verified')

class OrganizationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
