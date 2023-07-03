import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from .utils import generate_random_number_string



class UserManager(BaseUserManager):

    def create_user(self, email, firstname, lastname, password=None, ):
        if not all([firstname, lastname, password]):
            raise ValueError('Firstname, lastname and password are required.')
        account = generate_random_number_string()
        user = self.model(email=self.normalize_email(email), firstname=firstname, lastname=lastname, account_number=account )
        user.set_password(password)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_number = models.CharField(max_length=10, unique=True)
    email = models.CharField(("Email"), max_length=255, unique=True)
    firstname = models.CharField(max_length=255, default='')
    lastname = models.CharField(max_length=255, default='')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS= []

    objects = UserManager()

    def __str__(self) -> str:
        return self.account_number + ' - ' + self.firstname + ' ' + self.lastname

