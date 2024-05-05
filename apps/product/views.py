"""
Products related views
"""
# django import
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

# local import
from apps.common.msg import SUCCESS_KEY
from apps.common.utils import CustomResponse
from apps.common.viewsets import CustomModelViewSet
from apps.product.models import Product
from apps.product.serializers import ProductSerializer, ProductDetailsSerializer


class ProductViewSet(CustomModelViewSet):
    """
    API view for Products.

    This view set provides functionality for creating, retrieving,
     updating and deleting product.
    It uses the IsAuthenticated for permission checks.
    """
    serializer_class = ProductSerializer
    http_method_names = ('post', 'get', 'put', 'delete')
    permission_classes = [IsAuthenticated, ]
    queryset = Product
    filter_backends = (
        SearchFilter, DjangoFilterBackend, OrderingFilter
    )
    search_fields = ('title', 'description')
    ordering_fields = (
        'title', 'description', 'price', 'created_at'
    )

    def get_queryset(self):
        """
        Get custom queryset
        :return:
        """
        return Product.objects.filter(
            is_active=True, is_deleted=False).order_by('-created_at')

    def get_serializer_class(self):
        """
        get serializer class
        """
        serializer_class = self.serializer_class
        if self.action in ('list', 'retrieve'):
            serializer_class = ProductDetailsSerializer
        return serializer_class

    def create(self, request, *args, **kwargs):
        """
        To create a product
        :param request: post request object
        :param args: arguments
        :param kwargs: key arguments
        :return: json response
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(
                status.HTTP_201_CREATED, SUCCESS_KEY['product']['created']
            ).success_response()
        return CustomResponse(status.HTTP_400_BAD_REQUEST, serializer.errors).error_response()

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the details of a product.
        :param request: request object
        :param args: arguments
        :param kwargs: key arguments
        :return: json response
        """
        _ = request
        _ = args
        _ = kwargs
        instance = self.get_object()
        serializer = self.get_serializer(instance, many=False).data
        return CustomResponse(
            status.HTTP_200_OK
        ).success_response(serializer)

    def update(self, request, *args, **kwargs):
        """
        Updates the specified product with the new details.
        :param request: WSGI request.
        :return: The updated user object, or an error object
         if the update fails.
        """
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, data=request.data, partial=True,
            context={'product_id': instance.id}
        )

        # checking is there any error or not in serializer
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(
                status.HTTP_200_OK, SUCCESS_KEY['product']['updated']
            ).success_response()
        return CustomResponse(
            status.HTTP_400_BAD_REQUEST,
            serializer.errors
        ).error_response()

    def destroy(self, request, *args, **kwargs):
        """
        Destroy product based on its id
        """
        instance = self.get_object()
        instance.delete()
        return CustomResponse(
            status.HTTP_200_OK, SUCCESS_KEY['product']['deleted'],
        ).success_response()
