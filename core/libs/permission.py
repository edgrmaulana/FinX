import jwt

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated, BasePermission

from core.structures.project.models import Project, ProjectMember
from core.structures.role.models import Permission, Role
from enterprise.libs.rest_module.exception import ErrorValidationException

from django.conf import settings


class RBACPermission(BasePermission):
    message_error = {"en": "You don't have permission", "id": "Anda tidak punya akses"}

    def has_permission(self, request, view):
        # set false if not authenticated
        if not request.user.is_authenticated:
            raise ErrorValidationException(
                "401", {"en": "Unauthorized", "id": "Tidak terautentikasi"}, None, 401
            )

        # If user is super, return True
        if (
            request.user.is_authenticated
            and request.user.is_superuser
            or request.user.is_staff
        ):
            return True

        return self.has_permission_based_view(request, view)

    def has_permission_based_view(self, request, view):
        # Allow if user is superuser
        if request.user.is_superuser:
            return True

        # handle by permissions and always allow when not required permissions
        required_permissions = getattr(view, "required_permissions", {})
        required_permissions = required_permissions.get(view.action)

        if not required_permissions:
            return True

        # get user permission based on project and without project
        project_id62 = request.query_params.get("pid")
        project = Project.objects.filter(id62=project_id62, deleted_at__isnull=True)
        project_member = ProjectMember.objects.filter(
            project__id62=project_id62,
            project__deleted_at__isnull=True,
            user=request.user,
            deleted_at__isnull=True,
        )
        member_of_project = (
            project_member.exists() if request.user.is_authenticated else None
        )
        belongs_to_project = project or member_of_project
        if project_id62 and belongs_to_project:
            print("raise 1")
            raise ErrorValidationException(
                "403",
                self.message_error,
                None,
                403,
            )

        # get users permissions code names based on project role
        user_permissions = []
        if project_member:
            roles = project_member.last().roles
            for role in roles:
                user_permissions += role.get_permission_code_names()

        # raise error 403 if required permissions but user doesn't have permission
        if required_permissions and not user_permissions:
            print("raise 2")
            raise ErrorValidationException(
                "403",
                self.message_error,
                {"missing_permissions": required_permissions},
                403,
            )

        missing_permissions = []
        for required_permission in required_permissions:
            contain_permission = required_permission in user_permissions
            if not contain_permission:
                missing_permissions.append(required_permission)

        if missing_permissions:
            print("raise 3")
            raise ErrorValidationException(
                "403",
                self.message_error,
                {"missing_permissions": missing_permissions},
                403,
            )

        return True
