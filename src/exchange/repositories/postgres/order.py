from django.db import transaction
from datetime import datetime
from exchange.models import OrderQueue
from pytz import timezone


class OrderQueueRepository:
    @staticmethod
    def add_order_to_queue(crypto_name: str, amount: int, order_id: int) -> OrderQueue:
        """
        Adds an order to the queue and updates the total amount.

        Parameters
        ----------
        crypto_name : str
            The name of the cryptocurrency.
        amount : int
            The amount of the order.
        order_id : int
            The ID of the order.

        Returns
        -------
        OrderQueue
            The updated order queue.

        """
        with transaction.atomic():
            try:
                order_queue, _ = OrderQueue.objects.prefetch_related('orders').select_for_update().get_or_create(
                    crypto_name=crypto_name, is_deleted=False,
                    defaults=dict(total_amount=0))
                order_queue.orders.add(order_id)
                order_queue.total_amount += amount
                order_queue.save()
                return order_queue
            except Exception as e:
                print(e)
                transaction.set_rollback(True)
                raise e

    @staticmethod
    def mark_order_queue_as_paid(queue_id: int) -> None:
        """
        mark order queue as paid and set it is deleted
        :param queue_id:  queue id :
        :return:
        None
        """
        with transaction.atomic():
            try:
                OrderQueue.objects.select_for_update().filter(
                    id=queue_id).update(is_deleted=True, paid_at=datetime.now(tz=timezone('Asia/Tehran')))
            except Exception as e:
                print(e)
                transaction.set_rollback(True)
                raise e
