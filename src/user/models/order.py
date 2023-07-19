from django.core.exceptions import ValidationError
from django.db import models
from utils.model import BaseModel


def validate_balance(value: int) -> None:
    if value < 0 or value > 1000000:  # balance limitations
        raise ValidationError("Invalid balance.")


class Order(BaseModel):
    crypto_name = models.CharField(max_length=255)
    crypto_amount = models.PositiveIntegerField(validators=[validate_balance])
    processed = models.BooleanField(default=False)
    user = models.ForeignKey('user.User', on_delete=models.PROTECT)
