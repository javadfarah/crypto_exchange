from utils.model import BaseModel
from django.core.exceptions import ValidationError
from django.db import models


def validate_balance(value: int) -> None:
    """
    Validates the balance value.

    Parameters
    ----------
    value : int
        The balance value to be validated.

    Raises
    ------
    ValidationError
        If the balance value is less than 0 or greater than 1000000 (balance limitations).
    """
    if value < 0 or value > 1000000:  # balance limitations
        raise ValidationError("Invalid balance.")


class Balance(BaseModel):
    balance = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_balance])
    user = models.ForeignKey("user.User", on_delete=models.PROTECT)
