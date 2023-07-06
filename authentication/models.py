import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from .utils import generate_random_number_string
import random



class UserManager(BaseUserManager):

    def create_user(self, email, firstname, lastname, security_question, security_answer, password=None, *args, **kwargs):
        if not all([firstname, lastname, password]):
            raise ValueError('Firstname, lastname and password are required.')
        account = generate_random_number_string()
        user = self.model(email=self.normalize_email(email), firstname=firstname, lastname=lastname, account_number=account, security_question=security_question, security_answer=security_answer)
        user.set_password(password)
        user.username = user.generate_uniquie_username()
        user.save()
        return user
    
    def create_superuser(self, email, password, *args, **kwargs):
        if not all([email, password]):
            raise ValueError('Superusers must have a firstname, lastname, and password.')
        account = generate_random_number_string()
        user = self.model(email=self.normalize_email(email), account_number=account, firstname='', lastname='')
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractUser, PermissionsMixin):
    type = (
        ('What is your favorite food?', 'What is your favorite food?'),
        ('What is the name of your childhood friend?', 'What is the name of your childhood friend?'),
        ('What is the name of your first pet?', 'What is the name of your first pet?'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    account_number = models.CharField(max_length=10, unique=True)
    email = models.CharField(("Email"), max_length=255, unique=True)
    firstname = models.CharField(max_length=255, default='')
    lastname = models.CharField(max_length=255, default='')
    security_question = models.CharField(max_length=255)
    security_answer = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS= []

    objects = UserManager()

    def __str__(self) -> str:
        return self.account_number + ' - ' + self.firstname + ' ' + self.lastname

    def verify_security_answer(self, answer):
        return answer.lower() == self.security_answer.lower()
    
    def generate(self):
        ten_digits = str(random.randint(1000000000, 9999999999))
        return ten_digits
        
    def generate_uniquie_username(self):
        # Generates a unique username id
        unique_username = self.generate()
        
        # Filter user by the generated unique username id
        user = User.objects.filter(username=unique_username)
        if not user:
            username = unique_username
            return username


# 9b2da03c-69e8-44c3-8e7b-ad3f38fb463d