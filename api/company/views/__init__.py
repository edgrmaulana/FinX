from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from api.company.serializers.company import (
    CompanyListSerializer,
    CompanyWriteSerializer,
)

from core.libs.paginator import DRFPagination
from core.libs.managers.company import CompanyManager

from enterprise.libs.rest_module.response import DRFResponse

from enterprise.libs.rest_module.exception import ErrorValidationException


class CompanyViewSet(GenericViewSet):
    lookup_field = "id62"
    company_manager = CompanyManager()
    permission_classes = (IsAuthenticated,)
    pagination_class = DRFPagination

    def get_serializer_class(self):
        serializer_class = CompanyListSerializer

        if self.action in ["create", "update"]:
            serializer_class = CompanyWriteSerializer

        return serializer_class

    def create(self, request):
        """Create Company

        ## Payload
        ```
            {
                "display_name": "Company Foo Bar",
                "business_type": "Type",
                "address": {
                    "address": "Jalan Kenangan",
                    "postal_code": 55123,
                    "province": 12,
                    "regency": 1225,
                    "district": 1225060,
                    "village": 34762,
                    "lat_lng": "11,12"
                },
                "description": "Lorem Ipsum",
                "website": "https://company.dev",
                "logo": "D"
            }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        self.company_manager.create(**validated_data, created_by=request.user)

        response = DRFResponse(
            {"en": "Success create company", "id": "Sukses membuat company"}
        )

        return response.get_success_response("201", None, 201)

    def list(self, request):
        company_list = self.company_manager.list(created_by=request.user)
        page = self.paginate_queryset(company_list)
        serializer = self.get_serializer(page, many=True)
        data = self.paginator.get_paginated_response_dict(serializer.data)

        response = DRFResponse(
            {
                "en": "Success fetching company data",
                "id": "Berhasil mengambil data company",
            }
        )
        return response.get_success_response("200", data)

    def update(self, request, id62):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        company = self.company_manager.get_company(id62=id62)

        if not company:
            raise ErrorValidationException(
                "422",
                {"en": "Failed update company", "id": "Gagal mengubah perusahaan"},
                {"company": "company not found"},
                422,
            )

        self.company_manager.update(id62, **validated_data)
        response = DRFResponse(
            {"en": "Success update company", "id": "Sukses edit company"}
        )
        return response.get_success_response("201", None, 201)

    def destroy(self, request, id62):
        self.company_manager.delete(id62)
        response = DRFResponse(
            {"en": "Success delete company", "id": "Sukses hapus company"}
        )

        return response.get_success_response("201", None, 201)
