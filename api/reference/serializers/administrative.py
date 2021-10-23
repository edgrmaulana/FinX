from rest_framework import serializers
from enterprise.structures.administrative.models import (
    Province,
    Regency,
    District,
    Village,
)

DETAIL_UNAVAILABLE_MESSAGE = "Detail unavailable for this endpoint."


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ("id", "name", "postal_code")


class DistrictSerializer(serializers.ModelSerializer):
    village = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = ("id", "name", "village")

    def get_village(self, *args, **kwargs):
        if "village_serializer" in self._context:
            return self._context["village_serializer"].data
        else:
            return DETAIL_UNAVAILABLE_MESSAGE


class RegencySerializer(serializers.ModelSerializer):
    districts = serializers.SerializerMethodField()

    class Meta:
        model = Regency

        fields = ("id", "name", "districts")

    def get_districts(self, *args, **kwargs):
        if "district_serializer" in self._context:
            return self._context["district_serializer"].data
        else:
            return DETAIL_UNAVAILABLE_MESSAGE


class ProvinceSerializer(serializers.ModelSerializer):
    regencies = serializers.SerializerMethodField()

    class Meta:
        model = Province
        fields = ("id", "name", "regencies")

    def get_regencies(self, *args, **kwargs):
        if "regency_serializer" in self._context:
            return self._context["regency_serializer"].data
        else:
            return DETAIL_UNAVAILABLE_MESSAGE
