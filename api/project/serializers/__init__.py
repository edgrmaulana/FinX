from rest_framework import serializers

from core.structures.project.models import Project
from enterprise.libs.rest_module.exception import ErrorValidationException

from core.structures.role.models import Role
from core.structures.company.models import Company


class ProjectCreateSerializer(serializers.ModelSerializer):
    company = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = self.context["request"].user
        display_name = validated_data.get("display_name")
        company = validated_data.get("company")

        is_exists = Project.objects.filter(
            deleted_at__isnull=True, owned_by=user, display_name=display_name
        )

        if is_exists:
            raise ErrorValidationException(
                "422",
                {"en": "Project already exists", "id": "Project sudah ada"},
                {"project": f"{display_name} has already exists"},
                422,
            )

        company_instance = Company.objects.filter(
            id62=company, deleted_at__isnull=True, owned_by=user
        ).last()

        if not company_instance:
            raise ErrorValidationException(
                "422",
                {"en": "Failed create project", "id": "Gagal membuat project"},
                {"company": "Invalid Company"},
                422,
            )

        validated_data["company"] = company_instance
        return validated_data

    class Meta:
        model = Project
        fields = ("display_name", "active_services", "company")


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id62", "display_name", "active_services", "company")
