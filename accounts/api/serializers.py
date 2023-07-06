from rest_framework import serializers
from ..models import Account, Transaction


class AccountSerializers(serializers.ModelSerializer):

  class Meta:
    model = Account
    fields = '__all__'


class TransactionSerializers(serializers.ModelSerializer):
  amount = serializers.IntegerField()

  class Meta:
    model = Transaction
    fields = ['amount']

class TransferTransactionSerializers(serializers.Serializer):
  amount = serializers.IntegerField()
  account_number = serializers.IntegerField()

  