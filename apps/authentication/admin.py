"""
Authentication admin interface
"""
from django.contrib import admin

from apps.authentication.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    admin interface for User.
    """
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name')
