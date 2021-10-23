from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from enterprise.libs.rest_module.response import DRFResponse
from enterprise.libs.authentication import AuthenticationManager

from api.authentication.serializers.password import (
    ChangePasswordSerializer,
    SetPasswordSerializer,
)


class ChangePasswordViewset(GenericViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amer = AuthenticationManager()
        amer.set_passoword(request.user, serializer.validated_data.get("new_password"))

        response = DRFResponse(
            {"en": "Success change password", "id": "Perubahan kata sandi berhasil"}
        )
        response_dict = response.get_success_response("2000103", None)

        return response_dict


class SetPasswordViewset(GenericViewSet):
    """
    Oauth set password and forgot password.

    ### Requires
    * __type__ (available:"oauth", "forgot_password")
    * __forgot_token__ (code otp from email)
    """

    serializer_class = SetPasswordSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")

        amer = AuthenticationManager()
        amer.set_passoword(user, serializer.validated_data.get("password"))
        if serializer.validated_data.get("forgot_token"):
            response = DRFResponse(
                {"en": "Success change password", "id": "Perubahan kata sandi berhasil"}
            )
            response_dict = response.get_success_response("2000107", None)

        response = DRFResponse(
            {"en": "Success set password", "id": "pengaturan kata sandi berhasil"}
        )
        response_dict = response.get_success_response("2000106", None)

        return response_dict
