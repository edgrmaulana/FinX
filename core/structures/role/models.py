from django.db import models
from django.utils.translation import gettext_lazy as _

from enterprise.libs.base62 import base62_encode
from enterprise.libs.model import BaseModelGeneric


class Permission(models.Model):
    id62 = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    content_type_model = models.CharField(max_length=255)
    code_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        instance = super(Permission, self).save(*args, **kwargs)

        # generate id62
        if self.id and not self.id62:
            self.id62 = base62_encode(self.id)
            kwargs["force_insert"] = False
            instance = super(Permission, self).save(*args, **kwargs)

        return instance

    class meta:
        verbose_name = _("Permission")
        verbose_name_plural = _("Permissions")


class Role(BaseModelGeneric):
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE)
    display_name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(
        Permission, verbose_name=_("permissions"), blank=True
    )

    def get_permission_code_names(self):
        return list(self.permissions.values_list("code_name", flat=True))

    class meta:
        verbose_name = _("Project Role")
        verbose_name_plural = _("Project Roles")
