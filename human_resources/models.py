# from django.conf import settings
# from django.db import models
# from django.contrib.auth.models import Group, Permission


# class Department(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
#     )
#     name = models.CharField(max_length=255)
#     details = models.TextField(verbose_name="تفاصيل")

#     def __str__(self):
#         return f"self.id, self.name, self.details"


# class Branch(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         blank=True,
#         null=True,
#         verbose_name="",
#     )
#     name = models.CharField(max_length=255, verbose_name="اسم الفرع")
#     address = models.TextField(verbose_name="عنوان الفرع")
#     details = models.TextField(verbose_name="تفاصيل")

#     def __str__(self):
#         return f"self.id, self.name, self.address, self.details"


# # class Loan(models.Model):
# #     TYPE_CHOICES = [("general", "General"), ("emergency", "Emergency")]
# #     ACTION_CHOICES = [("approved", "Approved"), ("not approved", "Not-approved")]
# #     STATUS_CHOICES = [
# #         ("paid", "Paid"),
# #         ("partial paid", "Partial Paid"),
# #         ("not paid", "Not Paid"),
# #     ]
# #     user = models.ManyToManyField(
# #         settings.AUTH_USER_MODEL,
# #         on_delete=models.CASCADE,
# #         limit_choices_to={"is_superuser": True},
# #     )
# #     loan_type = models.CharField(choices=TYPE_CHOICES, max_length=10)
# #     loan_date = models.DateField(auto_now=True)
# #     amount = models.DecimalField(max_digits=5, decimal_places=2)
# #     monthly_installment = models.PositiveBigIntegerField(default=1)
# #     loan_batch = models.DecimalField(
# #         max_digits=5, decimal_places=2, blank=True, null=True
# #     )
# #     loan_remain = models.DecimalField(
# #         max_digits=5, decimal_places=2, blank=True, null=True
# #     )
# #     action = models.CharField(choices=ACTION_CHOICES, max_length=15)
# #     status = models.CharField(choices=STATUS_CHOICES)
# #     payment_date = models.DateField()
# #     description = models.TextField()


# class Loan(models.Model):
#     TYPE_CHOICES = [("general", "General"), ("emergency", "Emergency")]
#     ACTION_CHOICES = [("approved", "Approved"), ("not approved", "Not-approved")]
#     STATUS_CHOICES = [
#         ("paid", "Paid"),
#         ("partial paid", "Partial Paid"),
#         ("not paid", "Not Paid"),
#     ]
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         limit_choices_to={"is_superuser": True},
#     )
#     loan_type = models.CharField(choices=TYPE_CHOICES, max_length=10)
#     loan_date = models.DateField(auto_now=True)
#     amount = models.DecimalField(max_digits=5, decimal_places=2)
#     monthly_installment = models.PositiveIntegerField(default=1)
#     due = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
#     remain = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
#     action = models.CharField(choices=ACTION_CHOICES, max_length=15)
#     status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="not paid")
#     description = models.TextField()

#     def get_loan_data(self):
#         loan_data = {
#             "user_id": self.user.id,
#             "user_name": self.user.username,
#             "loan_type": self.loan_type,
#             "loan_date": self.loan_date,
#             "amount": self.amount,
#             "monthly_installment": self.monthly_installment,
#             "due": self.due,
#             "remain": self.remain,
#             "action": self.action,
#             "status": self.status,
#             "description": self.description,
#         }
#         return loan_data

#     def save(self, *args, **kwargs):
#         if self.action == "approved":
#             num_of_instalment_month = self.monthly_installment
#             self.due = self.amount / num_of_instalment_month
#             self.remain = self.amount
#             self.status = "not paid"
#         super().save(*args, **kwargs)

#     def __str__(self):
#         loan_data = self.get_loan_data()
#         return f"Loan ID: {self.id}, User ID: {loan_data['user_id']}, User Name: {loan_data['user_name']}, Loan Type: {loan_data['loan_type']}, Amount: {loan_data['amount']}, Monthly Installment: {loan_data['monthly_installment']}, Due: {loan_data['due']}, Remain: {loan_data['remain']}, Status: {loan_data['status']}"


# class Payment(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         limit_choices_to={"is_superuser": True},
#     )
#     loan = models.ManyToManyField(Loan, related_name="loans")
#     payment_date = models.DateField()
#     amount = models.DecimalField(max_digits=5, decimal_places=2)
#     due_date = models.DateField()

#     def save(self, *args, **kwargs):
#         # Check if the payment date is after the due date
#         if self.payment_date > self.due_date:
#             raise ValueError("Payment date cannot be after the due date")

#         # Deduct the payment amount from the user's salary
#         user = self.loan.user
#         user.salary -= self.amount
#         user.save()

#         super().save(*args, **kwargs)

#         # Update the loan status after saving the payment
#         payments = Payment.objects.filter(loan=self.loan).order_by("due_date")
#         total_payments = sum(payment.amount for payment in payments)
#         if total_payments >= self.loan.amount:
#             self.loan.status = "paid"
#             self.loan.remain = 0
#             self.loan.save()
#         elif total_payments >= self.loan.due:
#             self.loan.status = "partial paid"
#             self.loan.remain = self.loan.amount - total_payments
#             self.loan.save()

#     def __str__(self):
#         return f"Payment ID: {self.id}, Loan ID: {self.loan.id}, Payment Date: {self.payment_date}, Amount: {self.amount}, Due Date: {self.due_date}"


# class Pay_Roll(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         limit_choices_to={"is_superuser": True},
#     )
#     total_loan = models.PositiveBigIntegerField()
#     deduction = models.PositiveBigIntegerField()
#     basic_salary = models.PositiveBigIntegerField()
#     profit = models.PositiveBigIntegerField()
#     tax = models.PositiveBigIntegerField()
#     payment_date = models.DateField()
#     net_salary = models.PositiveBigIntegerField()


# class Role(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         limit_choices_to={"is_superuser": True},
#     )
#     name = models.CharField(max_length=255)
#     groups = models.ManyToManyField(Group)
#     permissions = models.ManyToManyField(Permission)

#     def add_user_permissions(self, user, permission):
#         user.user_permissions.add(permission)

#     def remove_user_permission(self, user, permission):
#         user.user_permissions.remove(permission)

#     def __str__(self):
#         return self.name
