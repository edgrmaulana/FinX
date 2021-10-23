from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from social_django.models import UserSocialAuth

from enterprise.libs.authentication import AuthenticationManager
from enterprise.libs.rest_module.response import DRFResponse

from api.authentication.serializers.login import (
    AuthenticateWithPasswordSerializer,
    CheckUsernameSerializer,
)


class AuthenticateWithPasswordView(GenericViewSet, mixins.CreateModelMixin):
    """
    Authenticate by Password.

    ### Requires
    * __phone_number__ (Always attach country code, _for example: 628581111_)
    * __password__
    * __device_id__ (A firebase device id)

    ### Return condition 1 (If user exist)
    * __token__ (Authorization token)

    ### Return condition 2 (If user doesn't exist)
    * __register_token__ (Register token is needed to register a user)

    ### Info
    Authorization token is needed to request authentication-required end-points.
    To use authorization token, you need to specify it in the header with format below.
    * e.g key: Authorization, value: Token <your-token>
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = AuthenticateWithPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        device_id = serializer.validated_data["device_id"]
        user = serializer.validated_data["user"]
        login_method = serializer.validated_data["login_method"]
        need_request_otp = serializer.validated_data["need_request_otp"]

        amer = AuthenticationManager()
        token = amer.generate_new_token(user)

        existing = UserSocialAuth.objects.filter(uid=device_id, provider="one").first()

        if existing:
            existing.delete()

        usa = UserSocialAuth(user=user, uid=device_id, provider="one")
        usa.save()

        # response
        response_manager = DRFResponse(
            {"en": "Successfully authenticated!", "id": "Login sukses!"}
        )
        response_dict = response_manager.get_success_response(
            "2000102",
            {
                "token": token.key,
                "login_method": login_method,
                "need_request_otp": need_request_otp,
            },
        )

        return response_dict


class CheckUsernameViewSet(GenericViewSet):
    serializer_class = CheckUsernameSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = DRFResponse({"en": "Username is valid", "id": "Username valid"})
        return response.get_success_response("2000104", serializer.validated_data)
