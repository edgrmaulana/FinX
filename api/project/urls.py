from django.conf.urls import url, include
from rest_framework import routers

from api.project.views import ProjectViewSet
from api.project.views.project_member import ProjectMemberViewSet

router = routers.DefaultRouter()
router.register(r"project", ProjectViewSet, "project")
router.register(r"member", ProjectMemberViewSet, "member")

urlpatterns = [
    url(r"", include(router.urls)),
]
