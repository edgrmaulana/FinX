from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny

from enterprise.libs import exceptions as custom_exceptions
from enterprise.libs.rest_module.response import DRFResponse
from enterprise.libs.authentication import AuthenticationManager

# from core.structures.account.models import Profile

from api.authentication.serializers.register import RegisterSerializers


class RegisterViewset(GenericViewSet):
    serializer_class = RegisterSerializers
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amer = AuthenticationManager()

        try:
            user = amer.basic_register(**serializer.validated_data)
        except custom_exceptions.PhoneNumberAlreadyExist:
            response = DRFResponse(
                {
                    "en": "phone number was alredy exist",
                    "id": "nomer telepon sudah terdaftar",
                }
            )
            return response.get_error_response(
                "4220109", serializer.validated_data, 422
            )
        except custom_exceptions.EmailAlreadyExist:
            response = DRFResponse(
                {
                    "en": "email alredy exist",
                    "id": "nomer telepon sudah terdaftar",
                }
            )
            return response.get_error_response(
                "4220108", serializer.validated_data, 422
            )

        response = DRFResponse({"en": "Success register", "id": "Pendaftaran berhasil"})
        serializer.validated_data.pop("password")

        # profile = user.objects.filter(deleted_at__isnull=True, owned_by=user).last()
        # if not profile:
        #     profile = user.objects.create(owned_by=user, created_by=user)

        response_dict = response.get_success_response(
            "2000103", serializer.validated_data
        )

        return response_dict
