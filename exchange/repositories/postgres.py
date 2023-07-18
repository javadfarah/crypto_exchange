from user.models import Balance
from django.db.models import F


class BalanceRepository:
    @staticmethod
    def check_if_user_balance_enough(user_id: int, balance: float) -> bool:
        return Balance.objects.filter(user_id=user_id, balance__gte=balance).exists()

    @staticmethod
    def decrease_user_balance(user_id: str, deduction_amount: int) -> None:
        Balance.objects.filter(user_id=user_id).update(balance=F('balance') - deduction_amount)
