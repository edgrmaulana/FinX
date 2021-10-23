from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from enterprise.libs.rest_module.viewsets.file_upload import (
    ChunkUploadViewSet,
    Base64UploadViewSet,
)
from api.reference.views import ContentTypeReferenceViewSet, AvailableServiceViewSet
from api.reference.views.administrative import (
    ProvinceViewSet,
    RegencyViewSet,
    DistrictViewSet,
    VillageViewSet,
)
from api.reference.views.country_code import CountryCodeViewSet

router = routers.DefaultRouter()
router.register(r"content-type", ContentTypeReferenceViewSet, "content-type")
router.register(r"available-service", AvailableServiceViewSet, "available-service")

# upload file
router.register(r"chunk-upload", ChunkUploadViewSet, "chunk-upload")
router.register(r"base64-upload", Base64UploadViewSet, "base64-upload")

# administrative
router.register(r"^province", ProvinceViewSet, "adminitrative-province")
router.register(r"^regency", RegencyViewSet, "adminitrative-regency")
router.register(r"^district", DistrictViewSet, "adminitrative-district")
router.register(r"^village", VillageViewSet, "adminitrative-village")

# country code
router.register(r"^country-code", CountryCodeViewSet, "country-code")

urlpatterns = [
    url(r"", include(router.urls)),
]
