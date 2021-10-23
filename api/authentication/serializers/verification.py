from rest_framework import serializers

from enterprise.libs.authentication import AuthenticationManager
from enterprise.libs.rest_module.exception import ErrorValidationException
from enterprise.libs.exceptions import (
    InvalidVerificationCode,
    ErrorSendingOTP,
    ErrorValidateOTP,
)
from enterprise.apps.authentication.templates import email as emailTemplate


class SendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data.get("email")
        email_lower = email.lower()

        amer = AuthenticationManager()
        user = amer._get_user("email", email_lower) or amer._get_user(
            "email", email_lower, False
        )

        if not user:
            raise ErrorValidationException(
                "4220101",
                {
                    "en": "email not found.",
                    "id": "email tidak ditemukan.",
                },
                validated_data,
                422,
            )

        # sending email verification
        email_subject = "email_verify.txt"
        email_template = "email_verify.html"

        code = amer.send_email_verification(user, email_subject, email_template, {})
        print(code)

        validated_data["user"] = user
        return validated_data


class SendPhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        phone_number = validated_data.get("phone_number")

        amer = AuthenticationManager()
        user = amer._get_user("phone_number", phone_number)
        is_valid = amer._phone_number_format_is_valid(phone_number)
        if not is_valid:
            raise ErrorValidationException(
                "4220107",
                {
                    "en": "Invalid phone number format",
                    "id": "Format nomor telepon tidak sesuai",
                },
                422,
            )

        if not user:
            raise ErrorValidationException(
                "4220114",
                {
                    "en": "phone number not found.",
                    "id": "phone number tidak ditemukan.",
                },
                validated_data,
                422,
            )

        try:
            _, request_id = amer.send_phone_verification(user=user)
        except ErrorSendingOTP as error:
            raise ErrorValidationException(
                "4220116",
                {
                    "en": "Failed sending OTP.",
                    "id": "Gagal mengirim OTP",
                },
                {"detail": str(error)},
                422,
            )

        validated_data["request_id"] = request_id
        return validated_data


class UserVerificationSerializer(serializers.Serializer):
    method = serializers.CharField()
    code = serializers.CharField()
    session_id = serializers.CharField(
        allow_null=True, allow_blank=True, required=False
    )

    def validate(self, attr):
        validated_data = super().validate(attr)

        method = validated_data.get("method")
        session_id = validated_data.get("session_id")
        error_message = {
            "en": "Failed to verify user",
            "id": "Gagal melakukan verifikasi user",
        }

        if method not in ["email", "phone_number"]:
            raise ErrorValidationException(
                "4220110",
                error_message,
                {"method": "available method email and phone_number"},
                422,
            )

        if method == "phone_number" and not session_id:
            raise ErrorValidationException(
                "4220117",
                error_message,
                {"session_id": "session_id required"},
                422,
            )

        amer = AuthenticationManager()
        try:
            value = validated_data.pop("code", None)
            user = amer.verify_user(**validated_data, value=value)
        except InvalidVerificationCode:
            raise ErrorValidationException(
                "4220113",
                error_message,
                {"code": "code invalid"},
                422,
            )
        except ErrorValidateOTP:
            raise ErrorValidationException(
                "4220118",
                error_message,
                {"code": "Failed verify OTP code"},
                422,
            )

        validated_data["response_dict"] = {
            "full_name": user.full_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "is_active": user.is_active,
            "token": amer.generate_new_token(user).key,
        }

        return validated_data
