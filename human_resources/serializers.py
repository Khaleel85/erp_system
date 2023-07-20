from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission
from core.models import (
    Department,
    Branch,
    Leave,
)
from django.utils import timezone
from datetime import timedelta, datetime


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


class LeaveCreateSerializer(serializers.ModelSerializer):
    leave_days = serializers.SerializerMethodField()

    class Meta:
        model = Leave
        fields = [
            "id",
            "leavetype",
            "startdate",
            "enddate",
            "reason",
            "defaultdays",
            "leave_days",
        ]
        read_only_fields = [
            "leave_days",
            "is_approved",
            "status",
            "created",
            "updated",
        ]

    def validate_startdate(self, value):
        today = timezone.now().date()
        three_days_from_today = today + timedelta(days=3)

        # Check if the leave type is "SICK" or "EMERGENCY" and start date is less than three days from today
        if self.initial_data.get("leavetype", "") in ["SICK", "EMERGENCY"] and value < three_days_from_today:
            return value

        if value < three_days_from_today:
            raise serializers.ValidationError(
                _("Leave request should be at least three days from today.")
            )
        return value

    def validate(self, data):
        startdate = data.get("startdate")
        enddate = data.get("enddate")

        if startdate and enddate and startdate > enddate:
            raise serializers.ValidationError(
                _("Start date cannot be greater than end date.")
            )

        return data

    def get_leave_days(self, obj):
        startdate = obj.startdate
        enddate = obj.enddate
        if startdate and enddate:
            return (enddate - startdate).days
        return 0


class LeaveDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = "__all__"  # Include all fields for updating

    def validate(self, data):
        startdate = data.get("startdate")
        enddate = data.get("enddate")
        if startdate and enddate and startdate > enddate:
            raise serializers.ValidationError(
                _("Start date cannot be greater than end date.")
            )
        return data
