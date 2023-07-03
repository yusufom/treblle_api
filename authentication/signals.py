from .models import User
from accounts.models import Account
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def created_account(sender, instance, created, **kwargs):
  if created:
    Account.objects.create(user=instance, balance=0)