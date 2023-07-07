from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from core.models import Department, Branch


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
