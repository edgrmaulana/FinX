from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import SerializerMethodField, ValidationError

from enterprise.libs.rest_module.serializer import LakonModelSerializer
from enterprise.structures.administrative.models import Address

DEFAULT_FIELD = ("id62", "nonce", "owned_by")
DEFAULT_FIELD_READ_ONLY = ("id62", "owned_by")
DEFAULT_FIELD_CREATE = ("id62", "nonce")


class AddressSerializer(LakonModelSerializer):
    province = SerializerMethodField()
    regency = SerializerMethodField()
    district = SerializerMethodField()
    village = SerializerMethodField()
    lat_lng = SerializerMethodField()

    class Meta:
        model = Address
        fields = (
            "address",
            "province",
            "regency",
            "district",
            "village",
            "postal_code",
            "lat_lng",
        )

    def get_province(self, obj):
        return (
            {"id": obj.province.id, "name": obj.province.name} if obj.province else None
        )

    def get_regency(self, obj):
        return {"id": obj.regency.id, "name": obj.regency.name} if obj.regency else None

    def get_district(self, obj):
        return (
            {"id": obj.district.id, "name": obj.district.name} if obj.district else None
        )

    def get_village(self, obj):
        return {"id": obj.village.id, "name": obj.village.name} if obj.village else None

    def get_lat_lng(self, obj):
        return obj.get_lat_lng()


class AddressWriteSerializer(LakonModelSerializer):
    class Meta:
        model = Address
        fields = (
            "address",
            "postal_code",
            "province",
            "regency",
            "district",
            "village",
            "lat_lng",
        )

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        try:
            latitude, longitude = validated_data.get("lat_lng").split(",")
        except ValueError:
            raise ValidationError(
                {"lat_lng": _("You should provide value like this: lat,lng")}
            )

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            raise ValidationError(
                {"lat_lng": _("Latitude and longitude must be float type")}
            )

        validated_data["lat_lng"] = "Point(%s %s)" % (longitude, latitude)

        return validated_data


class AddressReadSerializer(AddressWriteSerializer):
    province = SerializerMethodField()
    regency = SerializerMethodField()
    district = SerializerMethodField()
    village = SerializerMethodField()
    lat_lng = SerializerMethodField()

    def get_province(self, obj):
        return self.get_keyval(obj.province.id, obj.province.name)

    def get_regency(self, obj):
        return self.get_keyval(obj.regency.id, obj.regency.name)

    def get_district(self, obj):
        return self.get_keyval(obj.district.id, obj.district.name)

    def get_village(self, obj):
        return self.get_keyval(obj.village.id, obj.village.name)

    def get_lat_lng(self, obj):
        return obj.get_lat_lng("lat_lng")

    def get_keyval(self, key, val):
        return {"id": key, "text": val}
