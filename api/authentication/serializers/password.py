from rest_framework import serializers
from social_django.models import UserSocialAuth
from enterprise.libs.authentication import AuthenticationManager
from enterprise.libs.rest_module.exception import ErrorValidationException
from enterprise.libs.exceptions import InvalidVerificationCode


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user

        validated_data = super().validate(attrs)

        current_password = validated_data.get("current_password")
        new_password = validated_data.get("new_password")

        # let's check password format
        amer = AuthenticationManager()
        is_valid, error = amer._password_format_is_valid(new_password)
        if not is_valid:
            raise ErrorValidationException(
                "4220104",
                {
                    "en": "Invalid password format",
                    "id": "Format kata sandi tidak sesuai",
                },
                {"new_password": error},
                422,
            )

        if not amer.check_current_password(user, current_password):
            raise ErrorValidationException(
                "4220105",
                {
                    "en": "Failed change password, current password is incorrect",
                    "id": "Gagal mengubah kata sandi, kata sandi sebelumnya tidak sesuai",
                },
                {**validated_data},
                422,
            )

        return validated_data


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    type = serializers.CharField()
    forgot_token = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    def validate(self, data):
        request = self.context.get("request")
        user = request.user
        type_choice = ["oauth", "forgot_password"]
        password = data.get("password")
        type_method = data.get("type")
        forgot_token = data.get("forgot_token")

        data["user"] = user
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

        if type_method not in type_choice:
            raise ErrorValidationException(
                "4220110",
                {
                    "en": "Type invalid",
                    "id": "type tidak sesuai",
                },
                422,
            )
        if type_method == "oauth" and not user.is_authenticated:
            raise ErrorValidationException(
                "4030101",
                {
                    "en": "Account is forbidden access",
                    "id": "akun tidak mendapatkan izin akses",
                },
                403,
            )
        if type_method == "oauth":
            oauth = UserSocialAuth.objects.filter(user=user).last()

            if not oauth or (
                oauth and oauth.provider not in ["google-oauth2", "facebook"]
            ):
                raise ErrorValidationException(
                    "4220111",
                    {
                        "en": "oauth invalid",
                        "id": "validasi oauth tidak sesuai",
                    },
                    422,
                )
        if type_method == "forgot_password":
            if not forgot_token:
                raise ErrorValidationException(
                    "4220112",
                    {
                        "en": "forgot token can not null",
                        "id": "forgot token tidak boleh kosong",
                    },
                    422,
                )
            try:
                user = amer.verify_user("email", forgot_token)
            except InvalidVerificationCode:
                raise ErrorValidationException(
                    "4220113",
                    {
                        "en": "forgot token invalid",
                        "id": "validasi forgot token tidak sesuai",
                    },
                    422,
                )

            if not user:
                raise ErrorValidationException(
                    "4220113",
                    {
                        "en": "forgot token invalid",
                        "id": "validasi forgot token tidak sesuai",
                    },
                    422,
                )
            data["user"] = user

        return data
