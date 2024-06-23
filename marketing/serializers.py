from rest_framework import serializers
from .models import Organisation, Job

class OrganisationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'
        read_only_fields = ('id','email_verified')

class OrganisationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
