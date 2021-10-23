from django.conf.urls import url, include
from rest_framework import routers
from .views import CompanyViewSet

router = routers.DefaultRouter()
router.register(r"company", CompanyViewSet, "company")
urlpatterns = [
    url(r"", include(router.urls)),
]
