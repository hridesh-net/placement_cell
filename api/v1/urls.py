from django.urls import path
from django.urls import include
from applicants.views import ApplicantProfile as ApplicantProfile
from applicants.views import ApplicantView as Applicant


urlpatterns = [
    path("applicant/create/", Applicant.as_view(), name="create-applicant"),
]
