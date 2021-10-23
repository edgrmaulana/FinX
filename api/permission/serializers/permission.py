from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from core.structures.role.models import Permission
from enterprise.libs.base62 import base62_encode, base62_decode
from enterprise.libs.rest_module.exception import ErrorValidationException


class PermissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("name", "content_type_model", "code_name")


class PermissionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("id62", "name", "content_type_model", "code_name")
