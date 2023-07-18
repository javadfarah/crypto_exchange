from django.db import models
from utils.model import BaseModel


class Order(BaseModel):
    crypto_name = models.CharField(max_length=255)
    crypto_amount = models.PositiveIntegerField()
    processed = models.BooleanField(default=False)
    user = models.ForeignKey('user.User')
