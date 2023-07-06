from django.urls import path
from .views import AccountView, DepositView, WithdrawalView, TransferView

app_name = "core"

urlpatterns = [
    
    path('account/<str:id>/', AccountView.as_view(), name='account_balance'),
    path('deposit/<str:id>/', DepositView.as_view(), name='deposit'),
    path('withdraw/<str:id>/', WithdrawalView.as_view(), name='withdraw'),
    path('transfer/<str:id>/', TransferView.as_view(), name='transfer'),
]