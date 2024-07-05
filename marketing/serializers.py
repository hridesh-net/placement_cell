from rest_framework import serializers
from .models import Organisation, Job
from attachments.models import Attachment
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from attachments.serializers import AttachmentCreateSerializer

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['id', 'name', 'website', 'logo', 'contact_details',
                  'industry_type', 'location', 'created_by']

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
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.all(), source='company', write_only=True)
    attachments = serializers.ListField(
        child=serializers.FileField(), required=False, write_only=True)

    class Meta:
        model = Job
        fields = ['title', 'description', 'work_location', 'job_type', 'eligibility_criteria', 'deadline',
                  'stipend_salary', 'company_id', 'status', 'openings', 'custom_ques', 'perks_benefits', 'attachments']

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        job = Job.objects.create(**validated_data)

        for attachment_file in attachments_data:
            attachment_data = {
                'content_type': ContentType.objects.get_for_model(job),
                'object_id': job.id,
                'attachment_file': attachment_file,
                'attachment_type': 'resume'
            }
            Attachment.objects.create(**attachment_data)

        return job

    def update(self, instance, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        instance = super().update(instance, validated_data)

        for attachment_file in attachments_data:
            attachment_data = {
                'content_type': ContentType.objects.get_for_model(instance),
                'object_id': instance.id,
                'attachment_file': attachment_file,
                'attachment_type': 'resume'
            }
            Attachment.objects.create(**attachment_data)

        return instance


class JobGetSerializer(serializers.ModelSerializer):
    company = OrganisationSerializer()

    class Meta:
        model = Job
        fields = '__all__'
        depth = 1
