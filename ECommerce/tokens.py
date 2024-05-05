""" blacklist token class"""
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, BlacklistMixin, TokenError

from apps.authentication.models import UserAccessTokenBlacklisted


class AccessTokenBlacklistMixin:
    """
    If the `rest_framework_simplejwt.token_blacklist` app was configured to be
    used, tokens created from `AccessTokenBlacklistMixin` subclasses will insert
    themselves into an LogoutAccessToken list and also check for their
    membership in a token blacklist.
    """

    if "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS:
        def verify(self, *args, **kwargs):
            """ verifying token passed """
            self.check_blacklist()
            super().verify(*args, **kwargs)

        def check_blacklist(self):
            """
            Checks if this token is present in the token blacklist.  Raises
            `TokenError` if so.
            """
            jti = self.payload[api_settings.JTI_CLAIM]

            if UserAccessTokenBlacklisted.objects.filter(token__jti=jti).exists():
                raise TokenError(_("Token is blacklisted"))
            if UserAccessTokenBlacklisted.objects.filter(token__token=self.token.decode('utf-8')).exists():
                raise TokenError(_("Token is blacklisted"))


class JWTAccessToken(AccessTokenBlacklistMixin, BlacklistMixin, AccessToken):
    """ jwt access token """
    pass
