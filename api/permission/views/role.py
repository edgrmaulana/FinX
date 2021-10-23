from rest_framework.permissions import IsAuthenticated

from core.libs.viewsets.mixins import ListViewSet
from core.libs.filters import ProjectIDFilterBackend
from core.structures.role.models import Role
from enterprise.libs.rest_module.response import DRFResponse

from api.permission.serializers.role import RoleCreateSerializer, RoleListSerializer


class RoleViewSet(ListViewSet):
    lookup_field = "id62"
    permission_classes = (IsAuthenticated,)
    queryset = Role.objects.filter(deleted_at__isnull=True)
    filter_backends = (ProjectIDFilterBackend,)

    def get_serializer_class(self):
        serializer_class = RoleListSerializer
        if self.action == "create":
            serializer_class = RoleCreateSerializer

        return serializer_class

    def list(self, request):
        project_id62 = self.request.query_params.get("project_id62")
        self.queryset = self.get_queryset().filter(
            project__id62=project_id62, owned_by=request.user
        )

        return super().list(request)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        permissions = validated_data.pop("permissions")

        role = Role.objects.create(**serializer.validated_data, created_by=request.user)
        role.permissions.set(permissions)
        role.save()

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
