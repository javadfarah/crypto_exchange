from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .balance import Balance


class User(AbstractUser):
    class Meta:
        app_label = 'user'

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_user_balance_on_create(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(user=instance, balance=0)
