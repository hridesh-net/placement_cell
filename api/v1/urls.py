from django.urls import path
from django.urls import include

from applicants.views import (
    ApplicantView as Applicant,
    ApplicationView as Application,
    ApplicantProfileView as ApplicantProfile,
)
from accounts.views import LoginAPIView, SignupAPIView
from attachments.views import Attachment
from marketing.views import OrganisationView as Org, JobView as Job, VerifyOTPView

urlpatterns = [
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/signup/", SignupAPIView.as_view(), name="signup"),
    path("applicant/", Applicant.as_view(), name="create-applicant"),
    path(
        "applicantprofile/", ApplicantProfile.as_view(), name="create-applicant-profile"
    ),
    path("application/", Application.as_view(), name="create-app"),
    path("attachment/", Attachment.as_view(), name="create-attachment"),
    path("org/create/", Org.as_view(), name="create-organisation"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("job/", Job.as_view(), name="create-job"),
]
