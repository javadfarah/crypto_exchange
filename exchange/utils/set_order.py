from django.db import transaction
from rest_framework.response import Response

from exchange.repositories.postgres import OrderQueueRepository
from user.repositories.postgres.balance import BalanceRepository
from rest_framework import status
from django.core.exceptions import ValidationError

from user.repositories.postgres.order import OrderRepository


class OrderManager:
    def __init__(self, crypto_name: str, crypto_amount: int, user_id: int):
        self.crypto_name = crypto_name
        self.crypto_amount = crypto_amount
        self.user_id = user_id
        self.crypto_price = 4

    def get_total_amount(self) -> float:
        return self.crypto_amount * self.crypto_price

    def check_user_balance(self) -> None:
        if not BalanceRepository.check_if_user_balance_enough(user_id=self.user_id, balance=self.get_total_amount()):
            raise ValidationError("user balance is not enough.")

    def decrease_user_balance(self) -> None:
        BalanceRepository.decrease_user_balance(user_id=self.user_id, deduction_amount=self.get_total_amount())

    def process_orders(self) -> Response:
        self.check_user_balance()
        with transaction.atomic():
            self.decrease_user_balance()
            order = OrderRepository.create_order(crypto_name=self.crypto_name, user_id=self.user_id,
                                                 amount=self.crypto_amount)
            try:
                self.set_orders(order_id=order.id)
            except Exception as ee:
                print(ee)
                transaction.rollback()
                return Response({"message": "an error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": "Order saved and processed"})

    def set_orders(self, order_id: int) -> None:
        crypto_order_queue = OrderQueueRepository.add_order_to_queue(crypto_name=self.crypto_name,
                                                                     amount=self.crypto_amount, order_id=order_id)
        if crypto_order_queue.total_amount * self.crypto_price >= 10:
            if self.buy_from_exchange():
                OrderRepository.update_order_process_status(crypto_order_queue.orders, status=True)

    def buy_from_exchange(self) -> bool:
        return True
