from django.http import JsonResponse
from rest_api_payload import error_response
from rest_framework.response import Response
from rest_framework import status
from axes.helpers import get_cool_off_iso8601, get_cool_off, get_client_username
from django.conf import settings
from datetime import timedelta, datetime
from axes.models import AccessAttempt

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    return f"{hours} hour(s)"


def lockout(request, credentials, *args, **kwargs):

    value = convert_timedelta(get_cool_off())

    payload = error_response(
                status="failed",
                message=f"Account has been temporarily locked for security reasons. Please try again in {value}  or contact support if the problem persists. Thank you."
            )
            
    return Response(data=payload, status=status.HTTP_403_FORBIDDEN)

def get_client_ip(request):
    print(request.Meta)
    return request.META.get("REMOTE_ADDR")