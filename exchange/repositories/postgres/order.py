from exchange.models import OrderQueue
from user.models import Balance
from django.db.models import F


class OrderQueueRepository:
    @staticmethod
    def add_order_to_queue(crypto_name: str, amount: int, order_id: int) -> OrderQueue:
        order_queue, _ = OrderQueue.objects.prefetch_related('orders').select_for_update().get_or_create(
            defaults=dict(crypto_name=crypto_name, total_amount=0))
        order_queue.orders.add(order_id)
        order_queue.total_amount += amount
        order_queue.save()
        return order_queue
