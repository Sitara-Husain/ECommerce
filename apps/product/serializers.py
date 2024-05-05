"""
Product related serializers
"""
# django import
from rest_framework import serializers

# local import
from apps.common.msg import CHAR_LIMIT_SIZE, VALIDATION
from apps.product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Product related serializer
    """
    title = serializers.CharField(
        required=True,
        max_length=CHAR_LIMIT_SIZE["title"],
        error_messages=VALIDATION['title']
    )
    description = serializers.CharField(
        required=True,
        max_length=CHAR_LIMIT_SIZE["description"],
        error_messages=VALIDATION['description']
    )
    price = serializers.FloatField(
        required=True,
        error_messages=VALIDATION['price']
    )

    def validate_title(self, value):
        """
        validate title of product
        :return:
        """
        err = False
        product_id = self.context.get('product_id')
        product_obj = Product.objects.filter(title__iexact=value)
        if product_id and product_obj.exclude(id=product_id).exists():
            err = True
        elif not product_id and product_obj.exists():
            err = True
        if err:
            raise serializers.ValidationError(VALIDATION['title']['already_exists'])
        return value

    def create(self, validated_data):
        """
        create roadmap request for a student
        """
        return super(
            ProductSerializer, self
        ).create(validated_data)

    def update(self, instance, validated_data):
        """
        used to softly delete the Prize
        """
        return super(
            ProductSerializer,
            self
        ).update(instance, validated_data)

    class Meta:
        """
        Class meta for ProductSerializer
        """
        model = Product
        fields = ('title', 'description', 'price')


class ProductDetailsSerializer(serializers.ModelSerializer):
    """
    serializer class for product details
    """
    class Meta:
        """
        Class meta for ProductDetailsSerializer
        """
        model = Product
        fields = ('id', 'title', 'description', 'price')
