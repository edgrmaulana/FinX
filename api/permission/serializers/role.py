from rest_framework import permissions, serializers

from core.structures.project.models import Project
from core.structures.role.models import Role, Permission
from enterprise.libs.rest_module.exception import ErrorValidationException

from .permission import PermissionReadSerializer


class PermissionSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        id62 = validated_data.get("id62")
        permission = Permission.objects.filter(id62=id62).last()
        if not permission:
            raise ErrorValidationException(
                "422",
                {"en": "Invalid permission", "id": "Permission tidak valid"},
                {"permissions": f"{id62} invalid permission"},
            )

        validated_data["permission"] = permission
        return validated_data

    class Meta:
        model = Permission
        fields = ("id62",)


class RoleCreateSerializer(serializers.ModelSerializer):
    project = serializers.CharField()
    permissions = PermissionSerializer(many=True, required=False, allow_null=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        project = validated_data.get("project")
        permissions = validated_data.get("permissions")
        user = self.context["request"].user

        project = Project.objects.filter(
            deleted_at__isnull=True, id62=project, owned_by=user
        ).last()

        if not project:
            raise ErrorValidationException(
                "422",
                {"en": "Failed create data", "id": "Gagal menambah data"},
                {"project": "Project not found"},
                422,
            )

        if permissions:
            permissions = [p["permission"] for p in permissions]
        validated_data["permissions"] = permissions
        validated_data["project"] = project
        return validated_data

    class Meta:
        model = Role
        fields = ("project", "display_name", "permissions")


class RoleListSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, instance):
        serializer = PermissionReadSerializer(instance.permissions, many=True)

        return serializer.data

    def get_project(self, instance):
        return {
            "id62": instance.project.id62,
            "display_name": instance.project.display_name,
        }

    class Meta:
        model = Role
        fields = ("project", "display_name", "permissions")
