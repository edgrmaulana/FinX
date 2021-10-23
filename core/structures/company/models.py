from django.db import models

from enterprise.libs.model import BaseModelGeneric
from enterprise.structures.common.models import File
from enterprise.structures.administrative.models import Address


class Company(BaseModelGeneric):
    display_name = models.CharField(max_length=40)
    business_type = models.CharField(max_length=15)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    description = models.TextField()
    website = models.URLField(max_length=100)
    logo = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)

    class meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
