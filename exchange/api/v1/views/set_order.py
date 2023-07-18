from django.contrib.auth.models import User
from exchange.api.v1.serializers import SetOrderSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from user.models import Order
from django.db import transaction
from rest_framework.response import Response
from exchange.models import OrderQueue
from exchange.utils.set_order import OrderManager


class SetOrderView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SetOrderSerializer

    # this permission is mandatory but is commented for testing and development
    # permission_classes = [IsAuthenticated]
    crypto_price = 4

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        crypto_name = serializer.validated_data['crypto_name']
        crypto_amount = serializer.validated_data['crypto_amount']
        user_id = request.user.id
        OrderManager(crypto_name=crypto_name,crypto_amount=crypto_amount,user_id=user_id)
        return Response({"message": "Order saved"})

    def buy_from_exchange(self):
        return True