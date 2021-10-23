from rest_framework import serializers

from core.structures.company.models import Company
from enterprise.libs.base62 import base62_decode, base62_encode
from enterprise.libs.rest_module.exception import ErrorValidationException
from enterprise.structures.common.models import File

from api.company.serializers.address import (
    AddressWriteSerializer,
    AddressReadSerializer,
)


class CompanyListSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    def get_address(self, instance):
        if instance.address:
            return AddressReadSerializer(instance.address).data

        return None

    def get_logo(self, instance):
        if instance.logo:
            return {
                "id62": base62_encode(instance.logo_id),
                "url": instance.logo.get_safe_url(),
            }

    class Meta:
        model = Company
        fields = (
            "display_name",
            "business_type",
            "address",
            "description",
            "website",
            "logo",
        )


class CompanyWriteSerializer(serializers.ModelSerializer):
    logo = serializers.CharField()
    address = AddressWriteSerializer()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        logo = validated_data.get("logo")

        logo_file = File.objects.filter(id62=logo, deleted_at__isnull=True).last()

        if not logo_file:
            raise ErrorValidationException(
                "422",
                {"en": "Failed create company", "id": "Gagal membuat perusahaan"},
                {"logo": "Invalid file id62"},
                422,
            )

        validated_data["logo"] = logo_file
        return validated_data

    class Meta:
        model = Company
        fields = (
            "display_name",
            "business_type",
            "address",
            "description",
            "website",
            "logo",
        )
