import uuid
import os
import datetime

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


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
    EMPLOYMENT_CHOICES = [("Permanent", "permanent"), ("Contract", "contract")]
    GENDER_CHOICES = [("Male", "male"), ("Female", "female")]
    MARTIAL_STATUS_CHOICES = [
        ("Single", "single"),
        ("Married", "married"),
        ("Single Parent", "single parent"),
    ]
    MILITARY_CHOICES = [
        ("Finished Military Service", "finished military service"),
        (
            "Temporary Exemption from Military Service",
            "temporary exempted from military service",
        ),
        (
            "Final Exemption from Military Service",
            "final exemption from military service",
        ),
    ]
    mobile_num_regex = RegexValidator(
        regex="^[0-9]{11}$", message="Entered mobile number isn't in a right format!"
    )
    id_regex = RegexValidator(
        regex="^[0-9]{14}$", message="Entered ID number isn't in a right format!"
    )
    # user personal info
    email = models.EmailField(_("Email"), max_length=255, unique=True)
    name = models.CharField(_("Name"), max_length=255)
    name_ar = models.CharField(_("Name Arabic"), max_length=255, blank=True, null=True)
    name_unlang = models.CharField(
        _("Name Unlang"), max_length=255, blank=True, null=True
    )
    birthdate = models.DateField(_("Birthdate"), blank=True, null=True)

    identification = models.CharField(
        _("Identification"),
        validators=[id_regex],
        max_length=14,
        unique=True,
        blank=True,
        null=True,
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
    mobile_number = models.CharField(
        _("Mobile Number"),
        validators=[mobile_num_regex],
        unique=True,
        max_length=11,
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


# HR Models


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


class LeaveManager(models.Manager):
    def get_queryset(self):
        """
        overrides objects.all()
        return all leaves including pending or approved
        """
        return super().get_queryset()

    def all_pending_leaves(self):
        """
        gets all pending leaves -> Leave.objects.all_pending_leaves()
        """
        return (
            super().get_queryset().filter(status="pending").order_by("-created")
        )  # applying FIFO

    def all_cancel_leaves(self):
        return super().get_queryset().filter(status="cancelled").order_by("-created")

    def all_rejected_leaves(self):
        return super().get_queryset().filter(status="rejected").order_by("-created")

    def all_approved_leaves(self):
        """
        gets all approved leaves -> Leave.objects.all_approved_leaves()
        """
        return super().get_queryset().filter(status="approved")

    def current_year_leaves(self):
        """
        returns all leaves in current year; Leave.objects.all_leaves_current_year()
        or add all_leaves_current_year().count() -> int total
        this include leave approved,pending,rejected,cancelled

        """
        return super().get_queryset().filter(startdate__year=datetime.date.today().year)


class Leave(models.Model):
    LEAVE_TYPE = (
        ("SICK", "Sick Leave"),
        ("CASUAL", "Casual Leave"),
        ("EMERGENCY", "Emergency Leave"),
        ("STUDY", "Study Leave"),
    )
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Canceled", "Canceled"),
    )
    DAYS = 30
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    startdate = models.DateField(
        _("Start Date"),
        help_text=_("leave start date is on .."),
        null=True,
        blank=False,
    )
    enddate = models.DateField(
        _("End Date"),
        help_text=_("coming back on ..."),
        null=True,
        blank=False,
    )
    leavetype = models.CharField(
        choices=LEAVE_TYPE, max_length=25, default="SICK", null=True, blank=False
    )
    reason = models.TextField(
        _("Reason for Leave"),
        max_length=255,
        help_text=_("add additional information for leave"),
        null=True,
        blank=True,
    )
    defaultdays = models.PositiveIntegerField(
        _("Leave days per year counter"),
        default=DAYS,
        null=True,
        blank=True,
    )

    # hrcomments = models.ForeignKey('CommentLeave') #hide

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default="pending"
    )
    is_approved = models.BooleanField(default=False)  # hide

    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = LeaveManager()

    def leave_days(self):
        startdate = self.startdate
        enddate = self.enddate
        if startdate > enddate:
            raise ValueError("Start date cannot be greater than end date.")
        else:
            dates = (enddate - startdate).days
        return dates

    class Meta:
        verbose_name = _("Leave")
        verbose_name_plural = _("Leaves")
        ordering = ["-created"]  # recent objects

    def __str__(self):
        return "{0} - {1}".format(self.leavetype, self.user)



    @property
    def leave_days(self):
        startdate = self.startdate
        enddate = self.enddate
        if startdate and enddate:
            return (enddate - startdate).days + 1
        return 0
    @property
    def leave_approved(self):
        return self.is_approved == True

    @property
    def approve_leave(self):
        if not self.is_approved:
            self.is_approved = True
            self.status = "approved"
            self.save()

    @property
    def unapprove_leave(self):
        if self.is_approved:
            self.is_approved = False
            self.status = "pending"
            self.save()

    @property
    def leaves_cancel(self):
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = "cancelled"
            self.save()

    # def uncancel_leave(self):
    # 	if  self.is_approved or not self.is_approved:
    # 		self.is_approved = False
    # 		self.status = 'pending'
    # 		self.save()

    @property
    def reject_leave(self):
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = "rejected"
            self.save()

    @property
    def is_rejected(self):
        return self.status == "rejected"






# def save(self,*args,**kwargs):
# 	data = self.defaultdays
# 	days_left = data - self.leave_days
# 	self.defaultdays = days_left
# 	super().save(*args,**kwargs)


# class Comment(models.Model):
# 	leave = models.ForeignKey(Leave,on_delete=models.CASCADE,null=True,blank=True)
# 	comment = models.CharField(max_length=255,null=True,blank=True)

# 	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
# 	created = models.DateTimeField(auto_now=False, auto_now_add=True)


# 	def __str__(self):
# 		return self.leave


# # Account models
# class Customer(models.Model):
#     name = models.CharField(max_length=255)
#     # Add more fields as needed


# class Vendor(models.Model):
#     name = models.CharField(max_length=255)
#     # Add more fields as needed


# class AccountGroup(models.Model):
#     name = models.CharField(max_length=255)
#     parent_group = models.ForeignKey(
#         "self",
#         on_delete=models.CASCADE,
#         blank=True,
#         null=True,
#         related_name="child_groups",
#     )


# class Account(models.Model):
#     name = models.CharField(max_length=255)
#     account_group = models.ForeignKey(
#         AccountGroup, on_delete=models.CASCADE, related_name="accounts"
#     )


# class LedgerEntry(models.Model):
#     account = models.ForeignKey(
#         Account, on_delete=models.CASCADE, related_name="ledger_entries"
#     )
#     transaction_date = models.DateField(_())
#     description = models.TextField(_())
#     debit = models.DecimalField(_(), max_digits=12, decimal_places=2)
#     credit = models.DecimalField(_(), max_digits=12, decimal_places=2)
#     customer = models.ForeignKey(
#         Customer, on_delete=models.CASCADE, blank=True, null=True
#     )
#     vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)
