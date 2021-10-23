from django.conf import settings
from rest_framework import serializers

from enterprise.libs.jwt import JWTManager
from enterprise.structures.authentication.models import User


class RefreshTokenAuthenticationSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get("refresh_token")

        REFRESH_TOKEN_SECRET = getattr(settings, "REFRESH_TOKEN_SECRET", "s3jsd!ohd3gl")
        REFRESH_ALG = getattr(settings, "REFRESH_ALG", "HS256")
        jwt_manager = JWTManager(secret=REFRESH_TOKEN_SECRET, alg=REFRESH_ALG)

        is_success, decoded = jwt_manager.decode(token)
        if not is_success:
            raise serializers.ValidationError({"refresh_token": decoded})

        email = decoded.get("email")
        user = User.objects.filter(email=email).last()
        if not user:
            raise serializers.ValidationError({"refresh_token": "payload is invalid"})

        attrs["user"] = user

        return attrs


class AnonymousAuthenticationSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
