from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from core.models import Department, Branch, Pay_Roll, Role
from core.models import User
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(
        slug_field="name", queryset=Department.objects.all(), required=True
    )
    branch = serializers.SlugRelatedField(
        slug_field="name", queryset=Branch.objects.all(), required=True
    )
    basic_salary = serializers.SlugRelatedField(
        slug_field="basic_salary", queryset=Pay_Roll.objects.all(), required=True
    )
    role = serializers.SlugRelatedField(
        slug_field="name", queryset=Role.objects.all(), required=True
    )

    class Meta:
        model = get_user_model
        fields = [
            "email",
            "password",
            "name",
            "birthdate",
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
            "department",
            "branch",
            "position",
            "role",
            "basic_salary",
        ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        department_names = validated_data.pop("department")
        branch_names = validated_data.pop("branch")
        salary = validated_data.pop("basic_salary")
        role_names = validated_data.pop("role")
        try:
            department = Department.objects.get(name=department_names.strip())
            branch = Branch.objects.get(name=branch_names.strip())
            basic_salary = Pay_Roll.objects.get(name=salary.strip())
            role = Role.objects.get(name=role_names.strip())

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
        except Pay_Roll.DoesNotExist:
            raise serializers.ValidationError(
                {"salary": f'Salary "{salary}" Does Not exist.'}
            )
        except Pay_Roll.MultipleObjectsReturned:
            raise serializers.ValidationError(
                {"salary": f"Multiple salary with the name{salary} exist."}
            )
        except Role.DoesNotExist:
            raise serializers.ValidationError(
                {"role": f'Role "{role_names}" Does Not exist.'}
            )
        except Department.MultipleObjectsReturned:
            raise serializers.ValidationError(
                {
                    "department": f"Multiple departments with the name{department_names} exist."
                }
            )
        user = get_user_model().objects.create_user(
            department=department,
            branch=branch,
            basic_salary=basic_salary,
            role=role,
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
        fields = ["id", "image"]
        read_only_files = ["id"]
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
