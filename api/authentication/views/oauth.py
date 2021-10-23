from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny

from enterprise.libs.rest_module.response import DRFResponse
from api.authentication.serializers.oauth import SocialSerializer


class AuthenticateWithOauthView(GenericViewSet):
    """
    Authenticate with OAUTH.

    ### Requires
    * __access_token__
    * __backend__ (available:google-oauth2, facebook)

    ### Return
    * __token__ (Authorization token)

    ### Info
    Authorization token is needed to request authentication-required end-points.
    To use authorization token, you need to specify it in the header with format below.
    * e.g key: Authorization, value: Token <your-token>
    """

    permission_classes = (AllowAny,)
    serializer_class = SocialSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = serializer.validated_data.get("token")

        data_response = {
            "is_active": user.is_active,
            "email": user.email,
            "full_name": user.full_name,
            "token": token,
        }

        response_manager = DRFResponse(
            {"en": "Successfully authenticated!", "id": "Login sukses!"}
        )
        response_dict = response_manager.get_success_response("2000101", data_response)

        return response_dict
