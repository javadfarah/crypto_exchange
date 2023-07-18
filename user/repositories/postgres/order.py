from django.db.models import QuerySet

from user.models import Order


class OrderRepository:
    @staticmethod
    def update_order_process_status(orders: QuerySet, status: bool) -> None:
        orders.update(processed=True)

    @staticmethod
    def create_order(crypto_name: str, user_id: int, amount: int) -> Order:
        return Order.objects.create(crypto_name=crypto_name,
                                    user_id=user_id, crypto_amount=amount)
