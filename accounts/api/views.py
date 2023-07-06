from .serializers import AccountSerializers, TransactionSerializers, TransferTransactionSerializers
from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from rest_framework.views import APIView
from ..models import Account, Transaction
from rest_api_payload import error_response, success_response
from authentication.models import User
from rest_framework import generics, status
from ..throttle import TransferRateThrottle, WithdrawalRateThrottle
from django.db import IntegrityError, transaction


class AccountView(APIView):

  permissions_classes = [permissions.IsAuthenticated]
  
  def get(self, request, id, *args, **kwargs):
    """
    Get the user account with the id passed in the url, if it exists, it returns the account
    balance, if it doesn't exist, it returns an empty response
    
    :param request: The request object
    :param id: The id of the account to be retrieved
    :return: The get method is returning the account balance of the user.
    """
    try:
      user = User.objects.get(id=id)
      queryset = Account.objects.get(user=user)
      serializer = AccountSerializers(queryset)
      data = serializer.data
      data["account_number"] = user.account_number
      payload = success_response(
          status="success",
          message="Account Balance retrieved!",
          data=data
      )
      return Response(data=payload, status=status.HTTP_200_OK)
    except Account.DoesNotExist:
      payload = error_response(
          status="failed",
          message="Account Does not exist"
      )
      return Response(data=payload, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
      payload = error_response(
          status="failed",
          message="User Does not exist"
      )
      return Response(data=payload, status=status.HTTP_204_NO_CONTENT)

class DepositView(generics.GenericAPIView):
  serializer_class = TransactionSerializers
  permissions_classes = [permissions.IsAuthenticated]
  
  def post(self, request, id, *args, **kwargs):
    """
    It takes in a request, checks if the user and account exists, validates the data, checks if the
    amount is greater than 0, saves the data and returns a response
    
    :param request: The request object \n
    :param id: The id of the user whose account is to be credited \n
    :param amount: The amount to be deposited \n
    :return: A response object with the status code and the data
    """
    
    try:
      user = User.objects.get(id=id)
    except User.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

    try:
      account = Account.objects.get(user=user)
    except Account.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TransactionSerializers(data=request.data)

    if serializer.is_valid():
      deposit_amount = serializer.validated_data.get("amount")
      if deposit_amount >= 0:
        serializer.save(
          user = user,
          account = account,
          amount = deposit_amount,
          transaction_type = "D"
        )
        payload = success_response(
          status = "Success",
          message = f'${deposit_amount} successfully deposited',
          data = serializer.data
          )
        return Response(data=payload, status=status.HTTP_201_CREATED)
      else:
        payload = error_response (
          status  = 'failed',
          message = "Amount cannot be less than 0"
        )
        return Response(data=payload, status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class WithdrawalView(generics.GenericAPIView):
  serializer_class = TransactionSerializers
  throttle_classes = [WithdrawalRateThrottle]
  permissions_classes = [permissions.IsAuthenticated]
  
  def post(self, request, id, *args, **kwargs):
    """
    It checks if the user exists, if the account exists, if the amount is less than the balance, if
    the amount is greater than 0, and if all these conditions are met, it saves the transaction
    
    :param request: The request object \n
    :param id: This is the id of the user whose account is to be credited \n
    :param amount: This is the amount to be withdrawn \n
    :return: The transactor amount
    """
    try:
      user = User.objects.get(id=id)
    except User.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

    try:
      account = Account.objects.get(user=user)
    except Account.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TransactionSerializers(data=request.data)
    # serializer = TransactionSerializers(data=request.data)
    if serializer.is_valid():
      amount_withdrawn = serializer.validated_data.get("amount")
      if int(amount_withdrawn) > int(account.balance):
        payload =error_response(
          status = "Failed",
          message = "Amount can not be more than balance"
        )
        return Response(data=payload, status=status.HTTP_403_FORBIDDEN)
      elif int(amount_withdrawn) < 0:
        payload =error_response(
          status = "Failed",
          message = "Amount can not be less than 0"
        )
        return Response(data=payload, status=status.HTTP_403_FORBIDDEN)
      else:
        serializer.save(
          user = user,
          account = account,
          amount = amount_withdrawn,
          transaction_type = "W"
        )
        payload = success_response(
          status = "Success",
          message = f'${amount_withdrawn} successfully withdrawn',
          data = serializer.data
          )
        return Response(data=payload, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)
  


class TransferView(generics.GenericAPIView):
  serializer_class = TransferTransactionSerializers
  throttle_classes = [TransferRateThrottle]

  
  # permissions_classes = [permissions.IsAuthenticated]
  
  def post(self, request, id, *args, **kwargs):
    """
    It checks if the user exists, if the account exists, if the amount is less than the balance, if
    the amount is greater than 0, and if all these conditions are met, it saves the transaction
    
    :param request: The request object \n
    :param id: This is the id of the user whose account is to be credited \n
    :param amount: This is the amount to be withdrawn \n
    :return: The transactor amount
    """
    try:
      user = User.objects.get(id=id)
    except User.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

    try:
      account = Account.objects.get(user=user)
    except Account.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TransferTransactionSerializers(data=request.data)
    if serializer.is_valid():
      amount_withdrawn = serializer.validated_data.get("amount")
      account_number = serializer.validated_data.get("account_number")


      if int(amount_withdrawn) > int(account.balance):
        payload =error_response(
          status = "Failed",
          message = "Amount can not be more than balance"
        )
        return Response(data=payload, status=status.HTTP_403_FORBIDDEN)
      

      elif int(amount_withdrawn) < 0:
        payload =error_response(
          status = "Failed",
          message = "Amount can not be less than 0"
        )
        return Response(data=payload, status=status.HTTP_403_FORBIDDEN)
      

      else:
        with transaction.atomic():
          try:
            receiver = User.objects.get(account_number = account_number)
            print(account_number)
            receiver_account = Account.objects.get(user=receiver)
            receiver_account.balance += amount_withdrawn
            account.balance -= amount_withdrawn
            Transaction.objects.create(user=user, receiver=receiver, transaction_type="T", account=account, amount=amount_withdrawn)
            receiver.save()
            account.save()
          except User.DoesNotExist:
            return Response({"message": "Account number is wrong"})



        payload = success_response(
          status = "Success",
          message = f'${amount_withdrawn} successfully transfered',
          data = serializer.data
          )
        return Response(data=payload, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)