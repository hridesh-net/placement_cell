from django.urls import path
from django.urls import include

from applicants.views import ApplicantView as Applicant
from applicants.views import ApplicationView as Application
from attachments.views import Attachment

urlpatterns = [
    path("applicant/create/", Applicant.as_view(), name="create-applicant"),
    path("application/create/", Application.as_view(), name= "create-app"),
    path("attachment/create/", Attachment.as_view(), name="create-attachment"),
]
