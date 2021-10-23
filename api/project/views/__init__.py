from django.db import models
from rest_framework.permissions import IsAuthenticated

from core.libs.paginator import DRFPagination
from core.libs.viewsets.mixins import ListViewSet

from core.structures.project.models import Project, ProjectMember

from enterprise.libs.rest_module.response import DRFResponse
from enterprise.libs.rest_module.exception import ErrorValidationException

from api.project.serializers import ProjectCreateSerializer, ProjectListSerializer


class ProjectViewSet(ListViewSet):
    lookup_field = "id62"
    permission_classes = (IsAuthenticated,)
    pagination_class = DRFPagination
    queryset = Project.objects.filter(deleted_at__isnull=True)

    def list(self, request):
        user = request.user
        created_project = list(
            self.get_queryset().filter(owned_by=user).values_list("id", flat=True)
        )
        belongs_to_project = list(
            ProjectMember.objects.filter(
                deleted_at__isnull=True, user=user
            ).values_list("project_id", flat=True)
        )

        self.queryset = self.get_queryset().filter(
            id__in=created_project + belongs_to_project
        )

        return super().list(request)

    def get_serializer_class(self):
        serializer_class = ProjectListSerializer

        if self.action == "create":
            serializer_class = ProjectCreateSerializer

        return serializer_class

    def create(self, request):
        """
        ## Create Project Payload
        ```
           {
                "display_name": "Project Foo Bar",
                "active_services": [
                    "los"
                ],
                "company": "B"
            }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Project.objects.create(
            created_by=request.user, **serializer.validated_data, is_active=True
        )

        response = DRFResponse(
            {"en": "Success create data", "id": "Sukses menambah data"}
        )
        return response.get_success_response("201", None, 201)

    def update(self, request, id62=None):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        project = Project.objects.filter(id62=id62)

        if not project:
            raise ErrorValidationException(
                "422",
                {"en": "Failed update project", "id": "Gagal mengubah proyek"},
                {"project": "project not found"},
                422,
            )

        project.update(
            id62=validated_data.get("id62"),
            display_name=validated_data.get("display_name"),
            active_services=validated_data.get("active_services"),
        )

        response = DRFResponse(
            {"en": "Success update project", "id": "Sukses edit proyek"}
        )

        return response.get_success_response("201", None, 201)

    def destroy(self, request, id62=None):
        instance = self.get_object()
        instance.delete()

        response = DRFResponse(
            {"en": "Success delete project", "id": "Sukses hapus proyek"}
        )
        return response.get_success_response("201", None, 201)
