from rest_framework import serializers

from enterprise.libs import exceptions as custom_exceptions
from enterprise.libs.rest_module.exception import ErrorValidationException
from enterprise.libs.authentication import AuthenticationManager


class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )
    backend = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )

    def validate(self, data, *args, **kwargs):
        request = self.context["request"]
        access_token = data.get("access_token")
        backend = data.get("backend")

        amer = AuthenticationManager()

        try:
            user = amer.oauth_login(request, access_token, backend)
            user.is_active = True
            user.save()
        except custom_exceptions.InvalidOAuthBackend as err:
            raise ErrorValidationException(
                "4220103",
                {"en": "Invalid oauth backend", "id": "Invalid oauth backend"},
                str(err),
                422,
            )
        except Exception:
            raise ErrorValidationException(
                "4220106",
                {"en": "Access token invalid", "id": "Akses token tidak valid"},
                None,
                422,
            )

        token = amer.generate_new_token(user)

        data["user"] = user
        data["token"] = token.key
        return data
