import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from django.contrib.contenttypes.models import ContentType

from .models import *
from attachments.models import Attachment
from accounts.models import CustomUser


ATTACHMENT_TYPE = (
    ("resume", "Resume"),
    ("misc", "Miscellaneous"),
    ("academic", "Academic Docs"),
    ("photo_id", "Miscellaneous"),
    ("certificates", "Certificates"),
)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Faker("user_name")
    name = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall(
        "set_password", "password123"
    )  # Default password


class OrganisationFactory(DjangoModelFactory):
    class Meta:
        model = Organisation

    name = factory.Faker("company")
    website = factory.Faker("url")
    contact_details = factory.Faker("phone_number")
    industry_type = factory.Faker("company_suffix")
    location = factory.Faker("city")

    created_by = factory.SubFactory(UserFactory)


class AttachmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attachment

    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
    )
    object_id = factory.SelfAttribute("content_object.pk")
    attachment_file = factory.django.FileField(
        filename="sampledatapdf.pdf"
    )  # Provide a sample file
    attachment_type = factory.fuzzy.FuzzyChoice(
        [choice[0] for choice in ATTACHMENT_TYPE]
    )


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job

    title = factory.Faker("job")
    description = factory.Faker("text")
    work_location = factory.Faker("random_element", elements=["onsite", "remote"])
    job_type = factory.Faker("random_element", elements=["full_time", "part_time"])
    eligibility_criteria = factory.Faker("paragraph")
    deadline = factory.Faker("future_datetime", end_date="+30d")
    stipend_salary = factory.Faker(
        "random_element", elements=[None, "1000", "2000", "3000"]
    )
    company = factory.SubFactory(OrganisationFactory)
    status = factory.Faker("random_element", elements=["open", "closed"])
    openings = factory.Faker("random_int", min=1, max=10)
    perks_benefits = factory.Faker("paragraph")

    # Create attachments for the job
    @factory.post_generation
    def create_attachments(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for _ in range(extracted):
                AttachmentFactory(content_object=self)


user = UserFactory.create()
organisation = OrganisationFactory.create(created_by=user)
job = JobFactory.create(company=organisation)
