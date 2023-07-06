from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework import generics

# Create your views here.

class IndexView(generics.ListAPIView):
  permissions_classes = [permissions.AllowAny]

  
  def get(self, request):
    """
    It returns a dictionary of some of the endpoints in the API
    
    :param request: The request object passed in by the URL router
    :return: A dictionary with the keys being the endpoints and the values being the urls.
    """
    payload = {
        "Documentation" : "/docs",
        "login" : "/auth/api/login/",
        "register": "/auth/api/register/",
        "forgot-password": "/auth/api/forgot-password/",
        "reset-password": "/auth/api/reset-password/",
        "refresh-token": "/auth/api/token/refresh/",
        "withdraw": "/api/withdraw/{user_id}/",
        "deposit": "/api/deposit/{user_id}/",
        "balance": "/api/account/{user_id}/",
        "transfer": "/api/transfer/{user_id}/"
    }
    return Response(data=payload, status=status.HTTP_200_OK)