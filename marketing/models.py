from django.db import models
from attachments.models import Attachment
from django.contrib.contenttypes.fields import GenericRelation

from accounts.models import CustomUser

# Create your models here.

STATUS_CHOICES = [
    ("open", "Open"),
    ("closed", "Closed"),
]

LOCATION_TYPE = (
    ("remote", "Remote"),
    ("onsite", "Onsite"),
    ("hybrid", "Hybrid"),
)

JOB_TYPE = (
    ("part_time", "Part Time"),
    ("full_time", "Full Time"),
    ("internship", "Internship"),
)


class Organisation(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    logo = models.ImageField(upload_to="company_logos/", null=True, blank=True)
    contact_details = models.CharField(max_length=100, unique=True)
    industry_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    work_location = models.CharField(
        max_length=10, choices=LOCATION_TYPE, default="onsite"
    )
    job_type = models.CharField(
        max_length=10, choices=JOB_TYPE, default="full_time")
    eligibility_criteria = models.TextField()
    deadline = models.DateTimeField()
    stipend_salary = models.CharField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="open")
    openings = models.PositiveIntegerField(default=1)
    custom_ques = models.JSONField(blank=True, null=True)
    perks_benefits = models.TextField(blank=True, null=True)
    attachments = GenericRelation(Attachment)

    def __str__(self):
        return self.title
