from django.db import models
from utils.model import BaseModel


class OrderQueue(BaseModel):
    crypto_name = models.CharField(max_length=255)
    total_amount = models.PositiveIntegerField()
    orders = models.ManyToManyField('user.Order')
