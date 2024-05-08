from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(_("Email Address"), unique=True)
    name = models.CharField(_("Full Name"), max_length=20, default="Guest")
    phone_number = models.CharField(_("Contact Number"), max_length=15)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    objects = CustomUserManager()

    def __str__(self):
        return self.email
