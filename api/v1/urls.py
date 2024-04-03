from django.urls import path
from django.urls import include

from applicants.views import (
    ApplicantProfileView as ApplicantProfile,
    ApplicantView as Applicant,
    ApplicationView as Application,
)
from attachments.views import Attachment
from marketing.views import OrganisationView as Org, JobView as Job

urlpatterns = [
    path("applicant/", Applicant.as_view(), name="create-applicant"),
    path(
        "applicantprofile/", ApplicantProfile.as_view(), name="create-applicant-profile"
    ),
    path("application/", Application.as_view(), name="create-app"),
    path("attachment/", Attachment.as_view(), name="create-attachment"),
    path("org/create/", Org.as_view(), name="create-organisation"),
    path("job/", Job.as_view(), name="create-job"),
]
