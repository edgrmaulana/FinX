from django.contrib.contenttypes.models import ContentType

from core.libs import constants
from enterprise.libs.rest_module.viewsets.mixins import (
    ReferenceConstantMixin,
)


class ContentTypeReferenceViewSet(ReferenceConstantMixin):
    constant = constants.PERMISSION_MODEL_CHOICE
    queryset = ContentType.objects.all()
    value_text_field = {"value": "id", "text": "app_label"}


class AvailableServiceViewSet(ReferenceConstantMixin):
    constant = constants.SERVICE_CHOICES
