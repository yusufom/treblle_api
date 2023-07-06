from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import TokenRefreshSerializer, UserSerializer, LoginUserSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from axes.decorators import axes_dispatch
from axes.utils import reset
from axes.helpers import get_failure_limit
from axes.handlers.database import AxesDatabaseHandler
from rest_api_payload import success_response, error_response
from rest_framework import status
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from authentication.models import User
import re






from authentication.utils import get_ip

axes_handler = AxesDatabaseHandler()


# Create your views here.


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
class LoginView(generics.CreateAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = (permissions.AllowAny,)


    
    @method_decorator(axes_dispatch, name='dispatch')
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        if email and password:
            user = authenticate(request, email=email, password=password)
            if not user:
                f_limit = get_failure_limit(request, credentials={'username': email, 'ip': get_ip(request)})
                f_attempt = axes_handler.get_failures(request, credentials={'username': email, 'ip': get_ip(request)})

                attempt_left = int(f_limit) - int(f_attempt)

                attempt_msg = f"Invalid email address or password. {attempt_left} trie(s) left."
                if attempt_left == 1:
                    attempt_msg = "Invalid email address or password. Last chance, enter the correct email address and password to avoid a temporary account supension."
                elif attempt_left <= 0 :
                    attempt_msg = "Your account has been temporarily suspended due to multiple failed login attempts."

                payload = error_response(
                    status="failed",
                    message= attempt_msg
                )
                return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                refresh = RefreshToken.for_user(user)
                data = {
                    'user': UserSerializer(user, context=self.get_serializer_context()).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                payload = success_response(
                    status="success",
                    message="Login successful",
                    data=data
                )
                return Response(data=payload, status=status.HTTP_200_OK)


        payload = error_response(
                    status="failed",
                    message= "Something went wrong, Please try again"
                )
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

        
    
class TokenRefreshView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    
    

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data['refresh']

        token = RefreshToken(refresh)
        return Response({
            'access': str(token.access_token),
        })
    
    def get_serializer_class(self):
        return TokenRefreshSerializer
    
class ForgotPasswordView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ForgotPasswordSerializer

    

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        email = serializer.validated_data['email']
        security_question = serializer.validated_data['security_question']
        security_answer = serializer.validated_data['security_answer']

        try:
            user = User.objects.get(email=email)
            # if user.exists():
            if user.security_question == security_question and user.security_answer == security_answer:
                data = {
                    'email': user.email,
                }
                payload = success_response(
                    status="success",
                    message="Successful, Kindly proceed to change your password",
                    data=data
                )
                return Response(data=payload, status=status.HTTP_202_ACCEPTED)
            else:
                payload = error_response(
                    status="failed",
                    message= "Security question/answer does not match"
                )
                return Response(data=payload, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            payload = error_response(
                    status="failed",
                    message= "Invalid email address"
                )
            return Response(data=payload, status=status.HTTP_403_FORBIDDEN)
        
class ResetPasswordView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ResetPasswordSerializer

    

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        confirm_password = serializer.validated_data['confirm_password']

        password_message = True if password == confirm_password  else False

        try:
            user = User.objects.get(email=email)
            # if user.exists():
            if password_message is True:
                if re.fullmatch(r"[A-Za-z0-9@#$%^&+=-]{8,}", password):
                    user.password = password
                    user.set_password(password)
                    user.save()

                    payload = success_response(
                        status="success",
                        message="Successful, Your Password has been changed",
                    )
                    return Response(data=payload, status=status.HTTP_202_ACCEPTED)
                else:
                    payload = error_response(
                        status="failed",
                        message= "Your password is vulnerable, please try again"
                    )
                    return Response(data=payload, status=status.HTTP_403_FORBIDDEN)
            else:
                payload = error_response(
                        status="failed",
                        message= "Your password does not match"
                    )
                return Response(data=payload, status=status.HTTP_403_FORBIDDEN)

        except User.DoesNotExist:
            payload = error_response(
                    status="failed",
                    message= "Invalid user account"
                )
            return Response(data=payload, status=status.HTTP_403_FORBIDDEN)
