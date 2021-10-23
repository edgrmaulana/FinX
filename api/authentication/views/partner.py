from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from enterprise.libs.jwt import JWTManager
from core.structures.account.models import Profile
from enterprise.structures.authentication.models import User

from ..filters import GrantType
from ..serializers.write import (
    AnonymousAuthenticationSerializer,
    RefreshTokenAuthenticationSerializer,
)
from ..custom_authentication import MRTAuthentication


class AccessTokenViewSet(GenericViewSet):
    serializer_class = AnonymousAuthenticationSerializer
    filter_backends = (GrantType,)
    authentication_classes = (MRTAuthentication,)

    REFRESH_TOKEN_SECRET = getattr(settings, "REFRESH_TOKEN_SECRET", "s3jsd!ohd3gl")
    REFRESH_ALG = getattr(settings, "REFRESH_ALG", "HS256")
    REFRESH_EXP_HOURS = getattr(settings, "REFRESH_EXP_HOURS", 72)
    jwt_manager = JWTManager(secret=REFRESH_TOKEN_SECRET, alg=REFRESH_ALG)

    def _get_access_token(self, phone_number, full_name, email):
        user = User.objects.filter(email=email).last()
        if not user:
            user = User.objects.filter(phone_number=phone_number).last()

        if not user:
            user = User.objects.create(
                phone_number=phone_number, email=email, full_name=full_name
            )

        # create profile also
        profile = Profile.objects.filter(deleted_at__isnull=True, owned_by=user).last()
        if not profile:
            Profile.objects.create(created_by=user, owned_by=user)

        exp_in = timezone.now() + timedelta(hours=36)
        token = self.jwt_manager.encode({"id62": user.id62, "exp": exp_in})

        return token, user

    def _generate_refresh_token(self, email):
        exp_in = timezone.now() + timedelta(hours=self.REFRESH_EXP_HOURS)

        refresh_token = self.jwt_manager.encode({"email": email, "exp": exp_in})

        return refresh_token

    def create(self, request):
        grant_type = self.request.query_params.get("grant_type", "get_or_create")

        serializer_class = AnonymousAuthenticationSerializer
        if grant_type == "refresh_token":
            serializer_class = RefreshTokenAuthenticationSerializer

        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        response_dict = {"status": "success", "code": 200}
        if grant_type == "refresh_token":
            user = validated_data.get("user")
            token, _user = self._get_access_token(
                user.phone_number, email=user.email, full_name=user.full_name
            )
            response_dict = {
                **response_dict,
                "data": {
                    "access_token": token,
                    "refresh_token": self._generate_refresh_token(user.email),
                    "expired_at": timezone.now() + timedelta(hours=24),
                },
            }
        else:
            token, user = self._get_access_token(**validated_data)
            response_dict = {
                **response_dict,
                "data": {
                    "access_token": token,
                    "refresh_token": self._generate_refresh_token(user.email),
                    "expired_at": timezone.now() + timedelta(hours=24),
                },
            }

        return Response(response_dict)
