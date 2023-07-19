from django.db import transaction
from rest_framework.response import Response

from exchange.repositories.postgres import OrderQueueRepository
from user.repositories.postgres.balance import BalanceRepository
from rest_framework import status
from rest_framework.serializers import ValidationError
from abc import ABC, abstractmethod
from user.repositories.postgres.order import OrderRepository


class CommandInterface(ABC):
    @abstractmethod
    def start_process(self) -> Response:
        """
        Abstract method for starting the order processing.

        Returns
        -------
        Response
            Response object with the processing result.
        """
        pass


class OrderManager(CommandInterface):
    """
    Class responsible for managing order processing.

    Parameters
    ----------
    crypto_name : str
        The name of the cryptocurrency.
    crypto_amount : int
        The amount of cryptocurrency.
    user_id : int
        The user ID.
    """

    def __init__(self, crypto_name: str, crypto_amount: int, user_id: int):
        self.crypto_name = crypto_name
        self.crypto_amount = crypto_amount
        self.user_id = user_id
        self.crypto_price = 4

    def get_total_amount(self) -> float:
        """
        Calculates the total amount of the order.

        Returns
        -------
        float
            The total amount.
        """
        return self.crypto_amount * self.crypto_price

    def check_user_balance(self) -> None:
        """
        Checks if the user balance is enough to process the order.

        Raises
        ------
        ValidationError
            If the user balance is not enough.
        """
        if not BalanceRepository.check_if_user_balance_enough(user_id=self.user_id, balance=self.get_total_amount()):
            raise ValidationError("user balance is not enough.")

    def decrease_user_balance(self) -> None:
        """
        Decreases the user balance by the total amount of the order.
        """
        BalanceRepository.decrease_user_balance(user_id=self.user_id, deduction_amount=self.get_total_amount())

    def create_order(self):
        """
        Creates an order and returns it.

        Returns
        -------
        Order
            The created order.
        """
        return OrderRepository.create_order(crypto_name=self.crypto_name, user_id=self.user_id,
                                            amount=self.crypto_amount)

    def start_process(self) -> Response:
        """
        Starts the order processing.

        Returns
        -------
        Response
            Response object with the processing result.
        """
        self.check_user_balance()
        with transaction.atomic():
            self.decrease_user_balance()
            order = self.create_order()
            try:
                if self.set_orders(order_id=order.id) is True:
                    return Response({"message": "Order saved and processed"})
                else:
                    return Response({"message": "Order saved"})
            except Exception as ee:
                print(ee)
                transaction.set_rollback(True)
                return Response({"message": "an error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def set_orders(self, order_id: int) -> bool:
        """
        Sets the orders and checks if they can be processed.

        Parameters
        ----------
        order_id : int
            The ID of the created order.

        Returns
        -------
        bool
            True if the orders can be processed, False otherwise.
        """
        crypto_order_queue = OrderQueueRepository.add_order_to_queue(crypto_name=self.crypto_name,
                                                                     amount=self.crypto_amount, order_id=order_id)
        if crypto_order_queue.total_amount * self.crypto_price >= 10:
            if self.buy_from_exchange():
                OrderRepository.update_order_process_status(crypto_order_queue.orders, status=True)
                OrderQueueRepository.mark_order_queue_as_paid(crypto_order_queue.id)
                return True
        else:
            return False

    def buy_from_exchange(self) -> bool:
        """
        Simulates buying from the exchange.

        Returns
        -------
        bool
            True if the buying process is successful, False otherwise.
        """
        return True
