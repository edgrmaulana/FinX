from django.db import models, connection
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from api import project
from api.project.serializers.project_member import (
    ProjectMemberCreateSerializer,
    ProjectMemberListSerializer,
)
from core.libs.paginator import DRFPagination

from core.structures.project.models import ProjectMember
from enterprise.libs.rest_module.response import DRFResponse

from enterprise.libs.base62 import base62_decode


class ProjectMemberViewSet(GenericViewSet):
    lookup_field = "id62"
    permission_classes = (IsAuthenticated,)
    queryset = ProjectMember.objects.filter(deleted_at__isnull=True)
    pagination_class = DRFPagination

    def get_serializer_class(self):
        serializer_class = ProjectMemberCreateSerializer

        if self.action in ["list", "retrieve"]:
            serializer_class = ProjectMemberListSerializer

        return serializer_class

    def list(self, request):
        project_member_list = self.queryset.filter(owned_by_id=request.user)
        page = self.paginate_queryset(project_member_list)
        serializer = self.get_serializer(page, many=True)
        data = self.paginator.get_paginated_response_dict(serializer.data)

        response = DRFResponse(
            {
                "en": "Success fetching company data",
                "id": "Berhasil mengambil data company",
            }
        )
        return response.get_success_response("200", data)

    def retrieve(self, request, id62=None):
        """
        ### Get Project Member Based on Project ID
        Input id62 of project
        """
        id = base62_decode(id62)
        members = self.queryset.filter(project_id=id)
        page = self.paginate_queryset(members)
        serializer = self.get_serializer(page, many=True)
        data = self.paginator.get_paginated_response_dict(serializer.data)

        response = DRFResponse(
            {
                "en": "Success fetching permission data",
                "id": "Berhasil mengambil data project member",
            }
        )
        return response.get_success_response("200", data)

    def create(self, request):
        """
        ## Add Project's Member - Payload
        ```
           {
                "project": "C",
                "user_email": "user@example.com",
                "roles": [
                    {
                    "id62": "B"
                    }
                ]
            }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        user_email = validated_data["add_user"]
        project = validated_data["project"]
        role = validated_data["roles"]

        project_member = ProjectMember.objects.create(
            created_by=request.user, user_id=user_email.id, project_id=project.id
        )
        project_member.roles.set(role)
        project_member.save()

        response = DRFResponse(
            {"en": "Success create data", "id": "Sukses menambah data"}
        )
        return response.get_success_response("201", None, 201)

    def destroy(self, request, id62=None):
        instance = self.get_object()
        instance.delete()

        response = DRFResponse(
            {"en": "Success delete data", "id": "Sukses menghapus data"}
        )
        return response.get_success_response("200", None)
