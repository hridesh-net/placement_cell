from django.urls import path
from django.urls import include

from applicants.views import ApplicantView as Applicant
from marketing.views import OrganisationView as Org, JobView as Job


urlpatterns = [
    path("applicant/", Applicant.as_view(), name="create-applicant"),
    path("org/create/", Org.as_view(), name="create-organisation"),
    path("job/", Job.as_view(), name="create-job"),
]
