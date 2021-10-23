from django.db import models
from django.contrib.auth import get_user_model, models as auth_model
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from core.libs.constants import SERVICE_CHOICES
from core.structures.role.models import Role
from core.structures.company.models import Company

from enterprise.libs.model import BaseModelGeneric


class Project(BaseModelGeneric):
    display_name = models.CharField(max_length=200)
    active_services = ArrayField(
        models.CharField(max_length=32, blank=True, choices=SERVICE_CHOICES),
        default=list,
        blank=True,
    )
    is_active = models.BooleanField(default=False)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True
    )

    class meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class ProjectMember(BaseModelGeneric):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_user",
    )
    roles = models.ManyToManyField(Role)

    class meta:
        verbose_name = _("Project Member")
        verbose_name_plural = _("Project Members")
