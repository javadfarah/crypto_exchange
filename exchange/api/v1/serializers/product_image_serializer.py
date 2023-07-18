from rest_framework import serializers
from rest_framework.response import Response

from product.models import ProductImage
from django.core.files.base import ContentFile


class FileListSerializer(serializers.Serializer):
    image = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False)
    )

    def to_representation(self, instance):
        return ProductImageSerializer(instance, context=self.context).data

    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
