"""
Model file for authentication
"""
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.authentication.managers import UserManager
from apps.common.models import UuidTimeStampedModel


class User(AbstractBaseUser, PermissionsMixin, UuidTimeStampedModel):
    """
    A model representing a user account
    """
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(default=False)
    first_login_date = models.DateTimeField(null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def full_name(self):
        """
        To get user full name
        :return:
        """
        return f"{self.first_name} {self.last_name}"

    class Meta:
        """
        Meta options for the User model.
        """
        db_table = "auth_users"
        verbose_name = "Auth User"


class LogoutAccessToken(models.Model):
    """
    Logout Access Token
    """
    id = models.BigAutoField(primary_key=True, serialize=False)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="rel_user_logout"
    )
    jti = models.CharField(unique=True, max_length=255)
    token = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()

    class Meta:
        """
        Add metaclass
        """

        ordering = ("user",)

    def __str__(self):
        return "Token for {} ({})".format(
            self.user,
            self.jti,
        )


class UserAccessTokenBlacklisted(models.Model):
    """ User access token blacklist"""
    id = models.BigAutoField(primary_key=True, serialize=False)
    token = models.OneToOneField(LogoutAccessToken, on_delete=models.CASCADE)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blacklisted token for {self.token.user}"


class CustomUserAccessToken(models.Model):
    """ Custom User access token blacklist"""
    id = models.BigAutoField(primary_key=True, serialize=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rel_custom_user_access_token"
    )
    jti = models.CharField(max_length=255, blank=True, null=True)
    exp = models.CharField(max_length=255, blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    token = models.TextField(blank=True, null=True)

    class Meta:
        """
        Metadata for the CustomUserAccessToken model.
        """
        db_table = "custom_user_access_token"
