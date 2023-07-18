from rest_framework import serializers

from product.api.v1.serializers.product_image_serializer import FileListSerializer
from product.models import Product, ProductImage


class ProductSerializer(serializers.ModelSerializer):
    discount_percent = serializers.SerializerMethodField()
    discounted_percent = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_discount_percent(self, instance):
        return 0

    def get_discounted_percent(self, instance):
        return 0


class ProductSerializerRetrive(ProductSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1
