from rest_framework import serializers

from .models import Organisation, Job


class OrganisationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = "__all__"


class OrganisationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = "__all__"
        depth = 1
        # read_only_fields = ("id",)
        # extra_kwargs = {
        #     "jobs": {"required": False, "allow_null": True, "allow_empty": True}
        # }
        # exclude = ("id",)
        # read_only_fields = ("id",)
        # extra_kwargs = {
        #     "jobs": {"required": False, "allow_null": True, "allow_empty": True}
        # }
        # exclude = ("id",)
        # read_only_fields = ("id",)
        # extra_kwargs = {
        #     "jobs": {"required": False, "allow_null": True, "allow_empty": True}
        # }
        # exclude = ("id",)
        # read_only_fields = ("id",)
        # extra_kwargs = {
        #     "jobs": {"required": False, "allow_null": True, "allow_empty": True}
        # }
        # exclude = ("id",)


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"


class JobGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        depth = 1
