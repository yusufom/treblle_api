from rest_framework import generics, status, throttling




class TransferRateThrottle(throttling.UserRateThrottle):
    THROTTLE_RATES = {
        'user': '3/minute',  # Adjust the limit according to your needs
    }

class WithdrawalRateThrottle(throttling.UserRateThrottle):
    THROTTLE_RATES = {
        'user': '1/minute',  # Adjust the limit according to your needs
    }