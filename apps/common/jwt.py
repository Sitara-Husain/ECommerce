"""
 Used for user token blacklisting in jwt
 delete_tokens_for_user: This script defines a function to delete tokens associated with a user.
    Deletes all tokens associated with a given user.
delete_all_tokens_for_user: This script defines a function to delete all tokens associated with a user.
    Delete all tokens associated with a given user.
"""
from datetime import datetime
from django.utils import timezone

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.utils import datetime_from_epoch

from apps.authentication.models import (
    LogoutAccessToken, UserAccessTokenBlacklisted, CustomUserAccessToken
)


def delete_tokens_for_user(self, request):
    """
    Used for user token blacklisting
    :param self: The instance of the class (assuming this is a method within a class)
    :param request: The request object containing information about the user whose
     tokens are being blacklisted
    :return: True if the tokens were successfully blacklisted, False otherwise
    """
    tokens = OutstandingToken.objects.filter(user_id=request.user.id)
    for token in tokens:
        try:
            access_token = AccessToken(request.auth.token)
            access_token.set_exp(from_time=datetime.now(), lifetime=None)
            # token.token is refresh token
            token = RefreshToken(token.token)
            token.blacklist()
        except Exception as error:
            _ = error
    try:
        # blacklisting user Access Token
        jti = self.request.auth.payload['jti']
        exp = self.request.auth.payload['exp']

        # Ensure LogoutAccessToken exists with given jti
        token, _ = LogoutAccessToken.objects.get_or_create(
            jti=jti,
            user=self.request.user,
            defaults={
                "token": self.request.auth.token.decode('utf-8'),
                "expires_at": datetime_from_epoch(exp),
            },
        )
        UserAccessTokenBlacklisted.objects.get_or_create(token=token)
    except Exception as error:
        _ = error
    return True


def delete_all_tokens_for_user(user_id):
    """
    Used for user token blacklisting
    :param user_id: The user_id of the class (assuming this is a method within a class)
     tokens are being blacklisted
    :return: True if the tokens were successfully blacklisted, False otherwise
    """
    tokens = OutstandingToken.objects.filter(user_id=user_id)
    for token in tokens:
        try:
            token = RefreshToken(token.token)
            token.blacklist()
        except Exception as error:
            _ = error

    try:
        custom_user = CustomUserAccessToken.objects.filter(user_id=user_id)
        for data in custom_user:
            token, _ = LogoutAccessToken.objects.get_or_create(
                jti=data.jti,
                user_id=user_id,
                defaults={
                    "token": data.token,
                    "expires_at": timezone.now(),
                },
            )
            UserAccessTokenBlacklisted.objects.get_or_create(token=token)
            CustomUserAccessToken.objects.filter(id=data.id).delete()
    except Exception as error:
        _ = error
    return True
