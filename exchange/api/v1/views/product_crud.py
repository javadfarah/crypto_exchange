from product.api.v1.filters.product_crud_filters import ProductFilter
from product.api.v1.serializers.product_serializer import ProductSerializer, ProductSerializerRetrive
from product.models import Product
from rest_framework import viewsets
from django_filters import rest_framework as filters


class ProductCrud(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing customs.
    """

    queryset = Product.objects.filter().order_by('-id')
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializerRetrive
        if self.action == 'retrieve':
            return ProductSerializerRetrive
        return ProductSerializer
