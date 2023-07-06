from django.db import models
from authentication.models import User
from django.db import IntegrityError, transaction

# Create your models here.


class Account(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  balance = models.BigIntegerField()

  def __str__(self) -> str:
    return self.user.account_number


class Transaction(models.Model):
  type = (
        ('W', 'W'),
        ('D', 'D'),
        ('T', 'T'),
    )
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', null=True, blank=True)
  account = models.ForeignKey(Account, on_delete=models.CASCADE)
  transaction_type = models.CharField(max_length=255, blank=True, null=True, choices=type)
  amount = models.PositiveBigIntegerField()
  balance = models.PositiveBigIntegerField(null=True, blank=True)

  def __str__(self):
      return self.user.account_number
  


  def deposit(self):
    with transaction.atomic():
      user_account = Account.objects.get(user=self.user)
      print('yeah')
      if user_account:
        user_account.balance += int(self.amount)
        self.balance = user_account.balance
        user_account.save()

    

  def withdraw(self):
    with transaction.atomic():
      user_account = Account.objects.get(user=self.user)
      if user_account:
        user_account.balance -= int(self.amount)
        self.balance = user_account.balance
        user_account.save()


  def save(self, *args, **kwargs):
    if self.transaction_type == "W":
      self.withdraw()
    elif self.transaction_type == 'D':
      self.deposit()
    super(Transaction, self).save(*args, **kwargs)

# a52ddaeb-1597-422e-b5c2-2c0ccb01f8ca
# 4312775131