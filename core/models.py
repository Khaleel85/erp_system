from django.conf import settings
from django.contrib.auth.models import Group, Permission
import uuid
import os
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField

from django.utils.translation import gettext_lazy as _


def employee_photo_file_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "employee", filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    EMPLOYMENT_CHOICES = [("permanent", "Permanent"), ("contract", "Contract")]
    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]
    MARTIAL_STATUS_CHOICES = [
        ("single", "Single"),
        ("married", "Married"),
        ("single parent", "Single Parent"),
    ]
    MILITARY_CHOICES = [
        ("finished military service", "Finished Military Service"),
        (
            "temporary exemption from military service",
            "Temporary Exempted from Military Service",
        ),
        (
            "final exemption from military service",
            "Final Exemption from Military Service",
        ),
    ]
    # mobile_num_regex = RegexValidator(
    #     regex="^[0-9]{11}$", message="Entered mobile number isn't in a right format!"
    # )

    # user personal info
    email = models.EmailField(_("Email"), max_length=255, unique=True)
    name = models.CharField(_("Name"), max_length=255)
    birthdate = models.DateField(_("Birthdate"), blank=True, null=True)
    identification = models.PositiveIntegerField(
        _("Identification"), max_length=14, unique=True, blank=True, null=True
    )
    education = models.CharField(_("Education"), max_length=255, blank=True, null=True)
    recruitment = models.CharField(
        _("Military Service"),
        max_length=100,
        choices=MILITARY_CHOICES,
        blank=True,
        null=True,
    )
    gender = models.CharField(
        _("Gender"), max_length=6, choices=GENDER_CHOICES, default="male"
    )
    marital_status = models.CharField(
        _("Martial Status"), choices=MARTIAL_STATUS_CHOICES, max_length=13
    )
    home_address = models.TextField(_("Home Address"))
    mobile_number = PhoneNumberField(
        _("Mobile Number"),
        region="EG",
        unique=True,
        max_length=13,
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        _("Photo"),
        blank=True,
        null=True,
        upload_to=employee_photo_file_path,
    )

    # user's bank info
    bank_name = models.CharField(_("Bank Name"), max_length=255)
    bank_branch = models.CharField(_("Bank Branch"), max_length=255)
    bank_account_name = models.CharField(_("Bank account name"), max_length=255)
    bank_account_number = models.CharField(_("Bank account number"), max_length=255)

    # user's system info
    start_date = models.DateField(_("Start Date"), blank=True, null=True)
    employment_type = models.CharField(
        _("Employment Type"), max_length=10, choices=EMPLOYMENT_CHOICES
    )

    department_name = models.ForeignKey(
        "Department",
        on_delete=models.CASCADE,
        related_name="departments",
        verbose_name=_("Department Name"),
        blank=True,
        null=True,
    )
    branch_name = models.ForeignKey(
        "Branch",
        on_delete=models.CASCADE,
        related_name="branches",
        verbose_name=_("Branch Name"),
        blank=True,
        null=True,
    )

    position = models.CharField(_("Position"), max_length=255)
    is_active = models.BooleanField(_("Active Status"), default=True)
    is_staff = models.BooleanField(_("Is Staff"), default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Department(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    name = models.CharField(_("Department name"), max_length=255)
    details = models.TextField(_("Department Details"))

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    def __str__(self):
        return self.name


class Branch(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    name = models.CharField(_("Branch name"), max_length=255)
    address = models.TextField(_("Branch address"))
    details = models.TextField(_("Branch details"))

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")

    def __str__(self):
        return self.name
