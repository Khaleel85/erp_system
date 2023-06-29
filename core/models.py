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
from django.core.validators import RegexValidator

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
    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )

    # user personal info
    email = models.EmailField(_("Email"), max_length=255, unique=True)
    name = models.CharField(_("Name"), max_length=255)
    birthdate = models.DateField(_("Birthdate"), blank=True, null=True)
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
    basic_salary = models.ForeignKey(
        "Pay_Roll",
        on_delete=models.SET_NULL,
        related_name="salaries",
        blank=True,
        null=True,
    )

    department_name = models.ForeignKey(
        "Department",
        on_delete=models.CASCADE,
        related_name="departments",
        blank=True,
        null=True,
    )
    branch_name = models.ForeignKey(
        "Branch",
        on_delete=models.CASCADE,
        related_name="branches",
        blank=True,
        null=True,
    )
    role_name = models.ForeignKey(
        "Role",
        on_delete=models.CASCADE,
        related_name="roles",
        blank=True,
        null=True,
    )
    position = models.CharField(_("Position"), max_length=255)
    is_active = models.BooleanField(_("Active Status"), default=True)
    is_staff = models.BooleanField(_("Is Staff"), default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Department(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    name = models.CharField(_('Department name'),max_length=255)
    details = models.TextField(_('Department Details'))

    def __str__(self):
        return f"self.id, self.name, self.details"


class Branch(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    name = models.CharField(_('Branch name'),max_length=255)
    address = models.TextField(_('Branch address'))
    details = models.TextField(_('Branch details'))

    def __str__(self):
        return f"self.id, self.name, self.address, self.details"


# class Loan(models.Model):
#     TYPE_CHOICES = [("general", "General"), ("emergency", "Emergency")]
#     ACTION_CHOICES = [("approved", "Approved"), ("not approved", "Not-approved")]
#     STATUS_CHOICES = [
#         ("paid", "Paid"),
#         ("partial paid", "Partial Paid"),
#         ("not paid", "Not Paid"),
#     ]
#     user = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         limit_choices_to={"is_superuser": True},
#     )
#     loan_type = models.CharField(choices=TYPE_CHOICES, max_length=10)
#     loan_date = models.DateField(auto_now=True)
#     amount = models.DecimalField(max_digits=5, decimal_places=2)
#     monthly_installment = models.PositiveBigIntegerField(default=1)
#     loan_batch = models.DecimalField(
#         max_digits=5, decimal_places=2, blank=True, null=True
#     )
#     loan_remain = models.DecimalField(
#         max_digits=5, decimal_places=2, blank=True, null=True
#     )
#     action = models.CharField(choices=ACTION_CHOICES, max_length=15)
#     status = models.CharField(choices=STATUS_CHOICES)
#     payment_date = models.DateField()
#     description = models.TextField()


class Loan(models.Model):
    TYPE_CHOICES = [("general", "General"), ("emergency", "Emergency")]
    ACTION_CHOICES = [("approved", "Approved"), ("not approved", "Not-approved")]
    STATUS_CHOICES = [
        ("paid", "Paid"),
        ("partial paid", "Partial Paid"),
        ("not paid", "Not Paid"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"is_superuser": True},
    )
    loan_type = models.CharField(_('Loan Type'),choices=TYPE_CHOICES, max_length=10)
    loan_date = models.DateField(_('Loan date'),auto_now=True)
    amount = models.DecimalField(_('Amount'),max_digits=5, decimal_places=2)
    monthly_installment = models.PositiveIntegerField(_('Monthly Installment'),default=1)
    due = models.DecimalField(_('Due'),max_digits=5, decimal_places=2, blank=True, null=True)
    remain = models.DecimalField(_('Remain'),max_digits=5, decimal_places=2, blank=True, null=True)
    action = models.CharField(_('Action'),choices=ACTION_CHOICES, max_length=15)
    status = models.CharField(_('Loan Status'),max_length=50, choices=STATUS_CHOICES, default="not paid")
    description = models.TextField(_('Description'))

    def get_loan_data(self):
        loan_data = {
            "user_id": self.user.id,
            "user_name": self.user.username,
            "loan_type": self.loan_type,
            "loan_date": self.loan_date,
            "amount": self.amount,
            "monthly_installment": self.monthly_installment,
            "due": self.due,
            "remain": self.remain,
            "action": self.action,
            "status": self.status,
            "description": self.description,
        }
        return loan_data

    def save(self, *args, **kwargs):
        if self.action == "approved":
            num_of_instalment_month = self.monthly_installment
            self.due = self.amount / num_of_instalment_month
            self.remain = self.amount
            self.status = "not paid"
        super().save(*args, **kwargs)

    def __str__(self):
        loan_data = self.get_loan_data()
        return f"Loan ID: {self.id}, User ID: {loan_data['user_id']}, User Name: {loan_data['user_name']}, Loan Type: {loan_data['loan_type']}, Amount: {loan_data['amount']}, Monthly Installment: {loan_data['monthly_installment']}, Due: {loan_data['due']}, Remain: {loan_data['remain']}, Status: {loan_data['status']}"


class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"is_superuser": True},
    )
    loan = models.ManyToManyField(Loan, related_name="loans")
    payment_date = models.DateField(_('Payment day'))
    amount = models.DecimalField(_('Amount'),max_digits=5, decimal_places=2)
    due_date = models.DateField(_('Due date'))

    def save(self, *args, **kwargs):
        # Check if the payment date is after the due date
        if self.payment_date > self.due_date:
            raise ValueError("Payment date cannot be after the due date")

        # Deduct the payment amount from the user's salary
        user = self.loan.user
        user.salary -= self.amount
        user.save()

        super().save(*args, **kwargs)

        # Update the loan status after saving the payment
        payments = Payment.objects.filter(loan=self.loan).order_by("due_date")
        total_payments = sum(payment.amount for payment in payments)
        if total_payments >= self.loan.amount:
            self.loan.status = "paid"
            self.loan.remain = 0
            self.loan.save()
        elif total_payments >= self.loan.due:
            self.loan.status = "partial paid"
            self.loan.remain = self.loan.amount - total_payments
            self.loan.save()

    def __str__(self):
        return f"Payment ID: {self.id}, Loan ID: {self.loan.id}, Payment Date: {self.payment_date}, Amount: {self.amount}, Due Date: {self.due_date}"


class Pay_Roll(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"is_superuser": True},
    )
    total_loan = models.PositiveBigIntegerField(_('Total loan'))
    deduction = models.PositiveBigIntegerField(_('Deduction'))
    basic_salary = models.PositiveBigIntegerField(_('Basic Salary'))
    profit = models.PositiveBigIntegerField(_('Profit'))
    tax = models.PositiveBigIntegerField(_('Tax'))
    payment_date = models.DateField(_('Payment date'))
    net_salary = models.PositiveBigIntegerField(_('Net Salary'))


class Role(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"is_superuser": True},
    )
    name = models.CharField(_('Role name'),max_length=255)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission)

    def add_user_permissions(self, user, permission):
        user.user_permissions.add(permission)

    def remove_user_permission(self, user, permission):
        user.user_permissions.remove(permission)

    def __str__(self):
        return self.name
