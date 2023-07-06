from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from axes.decorators import axes_dispatch
from axes.utils import reset
from axes.helpers import get_failure_limit
from axes.handlers.database import AxesDatabaseHandler

from authentication.utils import get_ip

axes_handler = AxesDatabaseHandler()

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            security_answer=validated_data['security_answer'],
            security_question=validated_data['security_question'],
        )
        return user
    
    # def validate_security_answer(self, value):
    #     user = self.context['request'].user
    #     if not user.verify_security_answer(value):
    #         raise serializers.ValidationError('Invalid security answer')
    #     return value


    class Meta:
        model = User
        ref_name = "Auth User"
        fields = [ "id", "firstname", "lastname", "email", "password",'security_question', 'security_answer' ]
        
        extra_kwargs = {
            'password': {'write_only': True},
            'security_answer': {'write_only': True},
        }



class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh = data.get('refresh')

        if refresh:
            return data
        else:
            raise serializers.ValidationError('No refresh token provided.')

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    security_question = serializers.CharField()
    security_answer = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
