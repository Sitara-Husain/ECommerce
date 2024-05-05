"""
Product admin interface
"""
from django.contrib import admin

from apps.product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    admin interface for Product.
    """
    list_display = ('title', 'description', 'price')
    search_fields = ('title', )
