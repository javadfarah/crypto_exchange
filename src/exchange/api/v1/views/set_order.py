from user.models import Order
from exchange.api.v1.serializers import SetOrderSerializer
from rest_framework import generics
from exchange.utils.set_order import OrderManager


class SetOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = SetOrderSerializer
    # TODO: change the user_id section and get it from authenticated user
    # this permission is mandatory but is commented for testing and development
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        crypto_name = serializer.validated_data['crypto_name']
        crypto_amount = serializer.validated_data['crypto_amount']
        # user_id = request.user.id
        user_id = serializer.validated_data['user_id'].id
        order_manager = OrderManager(crypto_name=crypto_name, crypto_amount=crypto_amount, user_id=user_id)
        return order_manager.start_process()
