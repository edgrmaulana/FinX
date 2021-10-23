from rest_framework import serializers

from enterprise.libs.authentication import AuthenticationManager
from enterprise.libs.rest_module.exception import ErrorValidationException


class RegisterSerializers(serializers.Serializer):
    email = serializers.EmailField(max_length=150, required=True)
    phone_number = serializers.CharField(max_length=150, required=True)
    full_name = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=150, required=True)

    def validate(self, data):
        email = data.get("email")
        phone_number = data.get("phone_number")
        password = data.get("password")

        amer = AuthenticationManager()
        is_valid, error = amer._password_format_is_valid(password)
        if not is_valid:
            raise ErrorValidationException(
                "4220104",
                {
                    "en": "Invalid password format",
                    "id": "Format kata sandi tidak sesuai",
                },
                {"password": error},
                422,
            )

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

        is_registered = amer._get_user("email", email)
        if is_registered:
            raise ErrorValidationException(
                "4220108",
                {
                    "en": "email was alredy exist",
                    "id": "email sudah terdaftar",
                },
                422,
            )

        is_registered = amer._get_user("phone_number", phone_number)
        if is_registered:
            raise ErrorValidationException(
                "4220109",
                {
                    "en": "phone number alredy exist",
                    "id": "nomor telepon sudah terdaftar",
                },
                422,
            )

        return data
