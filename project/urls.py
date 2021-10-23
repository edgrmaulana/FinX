from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.urls import path
from django.contrib.flatpages import views

from django.contrib import admin
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


class RedirectVerifyView(RedirectView):
    query_string = True


urlpatterns = [
    path(
        "authentication/",
        include(
            ("api.authentication.urls", "authentication"), namespace="authentication"
        ),
    ),
    path(
        "company/",
        include(("api.company.urls", "company"), namespace="company"),
    ),
    path(
        "reference/",
        include(("api.reference.urls", "reference"), namespace="reference"),
    ),
    path(
        "permission/",
        include(("api.permission.urls", "permission"), namespace="permission"),
    ),
    path(
        "project/",
        include(("api.project.urls", "project"), namespace="project"),
    ),
]


if settings.DEBUG:
    admin.autodiscover()
    urlpatterns.append(url(r"^admin/", admin.site.urls))

    schema_view = get_schema_view(
        openapi.Info(
            title="Account FinX",
            default_version="v1",
            description="FinX's Account Service Documentation",
            contact=openapi.Contact(email="arif@sagara.asia"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        url=settings.BASE_URL,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns.append(
        url(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        )
    )
    urlpatterns.append(
        url(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        )
    )
    urlpatterns.append(
        url(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        )
    )

    urlpatterns.append(
        url(r"^", include(("apps.home.urls", "home"), namespace="home")),
    )

    urlpatterns = urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns.append(url(r"^", RedirectView.as_view(url="/swagger/")))
