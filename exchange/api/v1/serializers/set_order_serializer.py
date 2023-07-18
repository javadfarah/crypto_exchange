from rest_framework import serializers
from user.models import Order


class SetOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'