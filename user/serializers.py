from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from core.models import Department, Branch
from core.models import User
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    department_name = serializers.SlugRelatedField(
        slug_field="name", queryset=Department.objects.all(), required=True
    )
    branch_name = serializers.SlugRelatedField(
        slug_field="name", queryset=Branch.objects.all(), required=True
    )

    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "password",
            "name",
            "birthdate",
            "identification",
            "education",
            "recruitment",
            "gender",
            "marital_status",
            "home_address",
            "mobile_number",
            "photo",
            "bank_name",
            "bank_branch",
            "bank_account_name",
            "bank_account_number",
            "start_date",
            "employment_type",
            "department_name",
            "branch_name",
            "position",
        ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        department_names = validated_data.pop("department_name")
        branch_names = validated_data.pop("branch_name")
        department_name = department_names.name.strip()
        branch_name = branch_names.name.strip()

        try:
            department = Department.objects.get(name=department_name)
            branch = Branch.objects.get(name=branch_name)

        except Department.DoesNotExist:
            raise serializers.ValidationError(
                {"department": f'Department "{department_names}" Does Not exist.'}
            )
        except Department.MultipleObjectsReturned:
            raise serializers.ValidationError(
                {
                    "department": f"Multiple departments with the name{department_names} exist."
                }
            )
        except Branch.DoesNotExist:
            raise serializers.ValidationError(
                {"branch": f'Branch "{branch_names}" Does Not exist.'}
            )
        except Branch.MultipleObjectsReturned:
            raise serializers.ValidationError(
                {"Branch": f"Multiple branches with the name{branch_names} exist."}
            )

        user = get_user_model().objects.create_user(
            department_name=department,
            branch_name=branch,
            **validated_data,
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "photo"]
        read_only_fields = ["id"]
        extra_kwargs = {"photo": {"required": "True"}}


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs
