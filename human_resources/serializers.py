from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from core.models import Department, Branch, Loan, Payment, Pay_Roll, Role


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "details"]
        read_only_fields = ["id"]


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name", "details"]
        read_only_fields = ["id"]


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
            "loan_type",
            "loan_date",
            "amount",
            "monthly_installment",
            "due",
            "remain",
            "action",
            "status",
            "description",
        ]
        read_only_fields = ["id"]


class PayRollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay_Roll
        fields = [
            "id",
            "total_loan",
            "deduction",
            "basic_salary",
            "profit",
            "tax",
            "payment_date",
            "net_salary",
        ]
        read_only_fields = ["id"]


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

    def _get_or_create_permission(self, permissions, group):
        auth_user = self.context["request"].user
        for permission in permissions:
            permission_obj, created = Permission.objects.get_or_create(
                user=auth_user,
                **permission,
            )
            group.permission.add(permission_obj)

    def create(self, validated_data):
        permissions = validated_data.pop("permissions", [])
        group = Group.objects.create(**validated_data)
        self._get_or_create_permission(permissions, group)


class RoleSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, required=False)
    permissions = PermissionSerializer(many=True, required=False)

    class Meta:
        model = Role
        fields = ["id", "name", "groups", "permissions"]
        read_only_fields = ["id"]

    def _get_or_create_permission(self, permissions, role):
        auth_user = self.context["request"].user
        for permission in permissions:
            permission_obj, created = Permission.objects.get_or_create(
                user=auth_user,
                **permission,
            )
            role.permission.add(permission_obj)

    def create(self, validated_data):
        permissions = validated_data.pop("permissions", [])
        role = Role.objects.create(**validated_data)
        self._get_or_create_permission(permissions, role)
