# import uuid
# import os
# from django.db import models
# from django.contrib.auth.models import (
#     AbstractBaseUser,
#     BaseUserManager,
#     PermissionsMixin,
# )
# from django.core.validators import RegexValidator

# from django.utils.translation import gettext_lazy as _


# def employee_photo_file_path(instance, filename):
#     ext = os.path.splitext(filename)[1]
#     filename = f"{uuid.uuid4()}{ext}"
#     return os.path.join("uploads", "employee", filename)


# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("User must have an email address")
#         user = self.model(email=self.normalize_email(email), **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password):
#         user = self.create_user(email, password)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)

#         return user


# class User(AbstractBaseUser, PermissionsMixin):
#     EMPLOYMENT_CHOICES = [("permanent", "Permanent"), ("contract", "Contract")]
#     GENDER_CHOICES = [("male", "Male"), ("female", "Female")]
#     MARTIAL_STATUS_CHOICES = [
#         ("single", "Single"),
#         ("married", "Married"),
#         ("single parent", "Single Parent"),
#     ]
#     mobile_num_regex = RegexValidator(
#         regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
#     )

#     # user personal info
#     email = models.EmailField(
#         _('Email'),max_length=255, unique=True
#     )
#     name = models.CharField(_('Name'),max_length=255)
#     birthdate = models.DateField(_('Birthdate'))
#     gender = models.CharField(
#         _('Gender'),max_length=6, choices=GENDER_CHOICES, default="male"
#     )
#     marital_status = models.CharField(
#         _('Martial Status'),choices=MARTIAL_STATUS_CHOICES, max_length=13
#     )
#     home_address = models.TextField(_('Home Address'))
#     mobile_number = models.CharField(
#         _('Mobile Number'),
#         validators=[mobile_num_regex],
#         unique=True,
#         max_length=11,
#         blank=True,
#     )
#     photo = models.ImageField(
#         _('Photo'),
#         blank=True,
#         null=True,
#         upload_to=employee_photo_file_path,
#     )

#     # user's bank info
#     bank_name = models.CharField(_('Bank Name'),max_length=255)
#     bank_branch = models.CharField(_('Bank Branch'),max_length=255)
#     bank_account_name = models.CharField(
#         _('Bank account name'),max_length=255
#     )
#     bank_account_number = models.CharField(_('Bank account number'),max_length=255)

#     # user's system info
#     start_date = models.DateField(_('Start Date'))
#     employment_type = models.CharField(
#         _('Employment Type'),max_length=10, choices=EMPLOYMENT_CHOICES
#     )

#     position = models.CharField(_('Position'),max_length=255)
#     is_active = models.BooleanField(_('Active Status'),default=True)
#     is_staff = models.BooleanField(
#         _('Is Staff'),default=True
#     )

#     objects = UserManager()

#     USERNAME_FIELD = "email"
