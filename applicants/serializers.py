from rest_framework import serializers

from .models import Applicant, ApplicantProfile, Application, Skill
from accounts.serializers import UserGetSerializer


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"  # Include relevant skill fields

    def create(self, validated_data):
        # Check if skill already exists
        skill_name = validated_data["name"]
        existing_skill = Skill.objects.filter(name=skill_name).first()
        if not existing_skill:
            return Skill.objects.create(**validated_data)
        else:
            return existing_skill


class ApplicantCreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = "__all__"


class SkillManytoManySerializer(serializers.ManyRelatedField):
    queryset = Skill.objects.all()

    def create(self, validated_data):
        skills = []
        for skill_data in validated_data:
            skill_serializer = SkillSerializer(data=skill_data)
            skill_serializer.is_valid(raise_exception=True)
            skill = skill_serializer.save()
            skills.append(skill)
        return skills


class ApplicantProfileCreateSeializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantProfile
        fields = "__all__"

    def create(self, validated_data):
        # ... rest of your create method logic ...

        # Handle skills data using the custom ManyToManyField serializer
        skills_data = validated_data.pop("skills")
        skills = SkillManytoManySerializer(data=skills_data, many=True).create(
            skills_data
        )
        profile = ApplicantProfile.objects.create(**validated_data)
        profile.skills.set(skills)  # Set the skills for the profile

        return profile


class ApplicantProfileGetSerializer(serializers.ModelSerializer):
    applicant = UserGetSerializer(read_only=True)

    class Meta:
        model = ApplicantProfile
        fields = "__all__"
        depth = 1


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"


class ApplicationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        depth = 1
