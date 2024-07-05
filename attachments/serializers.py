from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Attachment, ATTACHMENT_TYPE

class AttachmentCreateSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(write_only=True)

    class Meta:
        model = Attachment
        fields = ("content_type", "object_id", "attachment_file", "attachment_type")

    def validate(self, data):
        content_type = data.get("content_type")
        object_id = data.get("object_id")
        if not (content_type and object_id):
            raise serializers.ValidationError("Both content_type and object_id are required.")

        try:
            ContentType.objects.get(model=content_type)
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("Invalid content_type provided.")

        return data

    def create(self, validated_data):
        content_type_str = validated_data.pop("content_type")
        content_type = ContentType.objects.get(model=content_type_str)

        return Attachment.objects.create(content_type=content_type, **validated_data)
