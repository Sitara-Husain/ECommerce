"""
Product models
"""
from django.db import models

from apps.common.models import TimeStampedModel


class Product(TimeStampedModel):
    """
    Model for storing products
    """
    title = models.CharField(null=True, blank=True, max_length=1024)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        """
        Metadata for the Note model.
        """
        db_table = "product"
        verbose_name = "Product"
