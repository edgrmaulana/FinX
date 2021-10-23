from rest_framework import serializers

from core.structures.project.models import Project, ProjectMember
from enterprise.libs.rest_module.exception import ErrorValidationException

from core.structures.role.models import Role
from django.contrib.auth import get_user_model


class RoleSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        id62 = validated_data.get("id62")
        role = Role.objects.filter(id62=id62).last()
        if not role:
            raise ErrorValidationException(
                "422",
                {"en": "Invalid roles", "id": "Role tidak valid"},
                {"permissions": f"{id62} invalid role"},
                422,
            )

        validated_data["role"] = role
        return validated_data

    class Meta:
        model = Role
        fields = ("id62",)


class ProjectMemberCreateSerializer(serializers.Serializer):
    project = serializers.CharField(required=True)
    user_email = serializers.CharField(required=True)
    roles = RoleSerializer(many=True, required=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = self.context["request"].user
        project = validated_data.get("project")
        roles = validated_data.get("roles")
        add_user_email = validated_data.get("user_email")

        added_user_exist = (
            get_user_model().objects.filter(is_active=True, email=add_user_email).last()
        )

        if not added_user_exist:
            raise ErrorValidationException(
                "422",
                {"en": "Added user not available",
                    "id": "Target user tidak ditemukan"},
                {"project": f"{add_user_email} don't exists"},
                422,
            )

        project_exist = Project.objects.filter(
            deleted_at__isnull=True, owned_by=user, id62=project
        ).last()

        if not project_exist:
            raise ErrorValidationException(
                "422",
                {"en": "Project dont exits", "id": "Tidak ada project"},
                {"project": f"{project} id62 don't exists"},
                422,
            )

        if roles:
            roles = [p["role"] for p in roles]

        validated_data["project"] = project_exist
        validated_data["add_user"] = added_user_exist
        validated_data["roles"] = roles

        return validated_data

    class Meta:
        model = ProjectMember
        fields = ("user_id", "project_id")


class ProjectMemberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ("id62", "project_id", "user_id",
                  "created_by", "owned_by_id", "roles")
