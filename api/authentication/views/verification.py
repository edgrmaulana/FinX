from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet


from enterprise.libs.rest_module.response import DRFResponse

from api.authentication.serializers.verification import (
    SendEmailVerificationSerializer,
    SendPhoneSerializer,
    UserVerificationSerializer,
)


class SendEmailVerificationViewSet(GenericViewSet):
    """
    Email Verification

    - after success register, trigger this endpoint to send email verification.
    - reset password via email. trigger this endpoint also
    """

    serializer_class = SendEmailVerificationSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = DRFResponse(
            {"en": "email verification sent", "id": "verifikasi email telah terkirim"}
        )
        return response.get_success_response("2000105", None)


class SendPhoneVerificationViewSet(GenericViewSet):
    """
    phone number Verification

    - after success register, trigger this endpoint to send phone number verification.
    """

    serializer_class = SendPhoneSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = DRFResponse(
            {
                "en": "phone number verification sent",
                "id": "verifikasi nomor telepon telah terkirim",
            }
        )
        return response.get_success_response("2000105", serializer.validated_data)


class VerifyUserViewSet(GenericViewSet):
    serializer_class = UserVerificationSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        response_dict = validated_data.get("response_dict")

        response = DRFResponse(
            {"en": "Success verify user", "id": "Verifikasi user berhasil"}
        )

        return response.get_success_response("2000108", response_dict)
