from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission
from core.models import (
    Department,
    Branch,
    Leave,
)


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


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = [
            "id",
            "startdate",
            "enddate",
            "leavetype",
            "reason",
            "defaultdays",
            "created",
            "updated",
        ]
        read_only_fields = ["is_approved", "status", "created", "updated"]

    def validate(self, data):
        startdate = data.get("startdate")
        enddate = data.get("enddate")
        if startdate and enddate and startdate > enddate:
            raise serializers.ValidationError(
                _("Start date cannot be greater than end date.")
            )
        return data
