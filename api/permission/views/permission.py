from rest_framework.generics import get_object_or_404

from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from core.libs.paginator import DRFPagination
from core.structures.role.models import Permission
from enterprise.libs.base62 import base62_decode, base62_encode
from enterprise.libs.rest_module.response import DRFResponse

from ..serializers.permission import (
    PermissionCreateSerializer,
    PermissionReadSerializer,
)


class PermissionViewSet(GenericViewSet):
    lookup_field = "id62"
    permission_classes = (IsAuthenticated,)
    queryset = Permission.objects.filter()
    pagination_class = DRFPagination

    def get_serializer_class(self):
        serializer_class = PermissionCreateSerializer

        if self.action in ["list", "retrieve"]:
            serializer_class = PermissionReadSerializer

        return serializer_class

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = DRFResponse(
            {"en": "Success create permission", "id": "Sukses membuat permission"}
        )

        return response.get_success_response("201", None, 201)

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = self.paginator.get_paginated_response_dict(serializer.data)

        response = DRFResponse(
            {
                "en": "Success fetching permission data",
                "id": "Berhasil mengambil data permission",
            }
        )
        return response.get_success_response("200", data)

    def retrieve(self, request, id62=None):
        id = base62_decode(id62)
        instance = get_object_or_404(self.get_queryset(), id=id)
        serializer = self.get_serializer(instance)

        response = DRFResponse(
            {
                "en": "Success fetching permission data",
                "id": "Berhasil mengambil data permission",
            }
        )
        return response.get_success_response("200", serializer.data)
