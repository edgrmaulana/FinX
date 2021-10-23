from django.conf.urls import url, include
from rest_framework import routers

from api.permission.views.permission import PermissionViewSet
from api.permission.views.role import RoleViewSet

router = routers.DefaultRouter()
router.register(r"permission", PermissionViewSet, "permission")
router.register(r"role", RoleViewSet, "role")

urlpatterns = [
    url(r"", include(router.urls)),
]
