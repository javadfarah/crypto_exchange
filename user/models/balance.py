from utils.model import BaseModel
from django.core.exceptions import ValidationError
from django.db import models


def validate_balance(value: int) -> None:
    if value < 0 or value > 1000000:  # balance limitations
        raise ValidationError("Invalid balance.")


class Balance(BaseModel):
    balance = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_balance])
    user = models.ForeignKey("user.User", on_delete=models.PROTECT)

    @property
    def balance_display(self):
        return "$%s" % self.balance
