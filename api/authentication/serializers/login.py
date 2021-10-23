from rest_framework import serializers

from enterprise.libs.authentication import AuthenticationManager
from enterprise.libs.rest_module.exception import ErrorValidationException
from enterprise.structures.authentication.models import PhoneVerification


class AuthenticateWithPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    device_id = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=150, required=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        amer = AuthenticationManager()
        user = amer._get_user("email", username)
        login_method = "email"

        if not user:
            user = amer._get_user("phone_number", username)
            login_method = "phone_number"

        if not user:
            raise ErrorValidationException(
                "4220101",
                {"en": "Authentication failed", "id": "Ontentikasi gagal"},
                {**data},
                422,
            )

        # password is valid?
        is_valid = user.check_password(password)

        if not is_valid:
            raise ErrorValidationException(
                "4220102",
                {"en": "Authentication failed", "id": "Ontentikasi gagal"},
                {**data},
                422,
            )

        need_request_otp = amer.user_has_verified(user, "phone_number")

        data["user"] = user
        data["login_method"] = login_method
        data["need_request_otp"] = bool(need_request_otp) == False

        return data

    class Meta:
        ref_name = "AuthenticateWithPasswordSerializer"


class CheckUsernameSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        username = validated_data.get("username")
        amer = AuthenticationManager()
        user = amer._get_user("email", username)
        method = "email"
        if not user:
            method = "phone_number"
            user = amer._get_user("phone_number", username)

        if not user:
            raise ErrorValidationException(
                "4220101",
                {
                    "en": "email or phone number not found.",
                    "id": "email atau nomor telepon tidak ditemukan.",
                },
                validated_data,
                422,
            )

        validated_data["username_type"] = method
        return validated_data
