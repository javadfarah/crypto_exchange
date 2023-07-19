from rest_framework import serializers
from user.models import Order, User


class SetOrderSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Order
        fields = ['crypto_name', 'crypto_amount', 'user_id']
