from rest_framework import serializers
from product.models import Feature


class FeatureSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(queryset=Feature.objects.all(),
                                                   many=False, allow_null=True)

    class Meta:
        model = Feature
        fields = ('id', 'name', 'parent_id', 'value', 'seo')

    def create(self, validated_data):
        parent = validated_data['parent_id']
        if parent:
            validated_data['parent_id'] = parent.id
        return Feature.objects.create(**validated_data)
