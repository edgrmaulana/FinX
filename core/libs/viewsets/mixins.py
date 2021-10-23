from rest_framework.viewsets import GenericViewSet

from core.libs.paginator import DRFPagination
from enterprise.libs.rest_module.response import DRFResponse


class ListViewSet(GenericViewSet):
    lookup_field = "id62"
    pagination_class = DRFPagination
    paginator_data = []

    def list(self, request):
        queryset = self.queryset
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        self.paginator_data = self.paginator.get_paginated_response_dict(
            serializer.data
        )

        response = DRFResponse(
            {
                "en": "Success fetching data",
                "id": "Berhasil mengambil data",
            }
        )
        return response.get_success_response("200", self.paginator_data)
