from rest_framework.viewsets import GenericViewSet, mixins

from core.libs.paginator import DRFPagination
from core.libs.filters import (
    ProvinceIDFilterBackend,
    RegencyIDFilterBackend,
    DistrictIDFilterBackend,
)
from enterprise.libs.rest_module.response import DRFResponse
from enterprise.structures.administrative.models import (
    Province,
    Regency,
    District,
    Village,
)

from ..serializers.administrative import (
    ProvinceSerializer,
    RegencySerializer,
    DistrictSerializer,
    VillageSerializer,
)


class AdministrativeViewSetMixins(GenericViewSet, mixins.ListModelMixin):
    pagination_class = DRFPagination

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = self.paginator.get_paginated_response_dict(serializer.data)

        response = DRFResponse(
            {
                "en": "Success fetching data",
                "id": "Berhasil mengambil data",
            }
        )
        return response.get_success_response("200", data)


class ProvinceViewSet(AdministrativeViewSetMixins):
    serializer_class = ProvinceSerializer
    queryset = Province.objects.all()


class RegencyViewSet(AdministrativeViewSetMixins):
    serializer_class = RegencySerializer
    filter_backends = (ProvinceIDFilterBackend,)

    def get_queryset(self):
        province_id = self.request.query_params.get("province_id")
        return Regency.objects.filter(province_id=province_id)


class DistrictViewSet(AdministrativeViewSetMixins):
    serializer_class = DistrictSerializer
    filter_backends = (RegencyIDFilterBackend,)

    def get_queryset(self):
        regency_id = self.request.query_params.get("regency_id")
        return District.objects.filter(regency_id=regency_id)


class VillageViewSet(AdministrativeViewSetMixins):
    serializer_class = VillageSerializer
    filter_backends = (DistrictIDFilterBackend,)

    def get_queryset(self):
        district_id = self.request.query_params.get("district_id")
        return Village.objects.filter(district_id=district_id)
