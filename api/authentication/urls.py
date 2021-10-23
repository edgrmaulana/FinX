"""
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: urls.py
# Project: api.lakon.app
# File Created: Monday, 10th September 2018 2:51:14 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Monday, 10th September 2018 2:51:15 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Hand-crafted & Made with Love
# Copyright - 2018 Lakon, lakon.app
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""


from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from api.authentication.views.login import (
    AuthenticateWithPasswordView,
    CheckUsernameViewSet,
)
from api.authentication.views.oauth import AuthenticateWithOauthView
from api.authentication.views.password import (
    ChangePasswordViewset,
    SetPasswordViewset,
)
from api.authentication.views.register import RegisterViewset
from api.authentication.views.verification import (
    SendEmailVerificationViewSet,
    SendPhoneVerificationViewSet,
    VerifyUserViewSet,
)

router = routers.DefaultRouter()
router.register(
    r"authenticate/password", AuthenticateWithPasswordView, "authenticate-password"
)
router.register(r"authenticate/oauth", AuthenticateWithOauthView, "authenticate-oauth")
router.register(
    r"authenticate/send-email-verification",
    SendEmailVerificationViewSet,
    "authenticate-send-email-verification",
)
router.register(
    r"authenticate/send-phone-verification",
    SendPhoneVerificationViewSet,
    "authenticate-send-phone-verification",
)
router.register(r"authenticate/check-username", CheckUsernameViewSet, "check-username")
router.register(
    r"authenticate/change-password",
    ChangePasswordViewset,
    "authenticate-change-password",
)
router.register(
    r"authenticate/set-password",
    SetPasswordViewset,
    "set-password",
)
router.register(
    r"authenticate/basic-register",
    RegisterViewset,
    "basic-register",
)
router.register(
    r"authenticate/verify-user",
    VerifyUserViewSet,
    "verify-user",
)
urlpatterns = [
    url(r"", include(router.urls)),
]
