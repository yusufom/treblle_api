from django.test import TestCase
from .utils import generate_random_number_string
from .models import *
import pytest
from django.db import IntegrityError

# Create your tests here.
class GenerateTenString(TestCase):
    def test_string_length(self):
        assert len(generate_random_number_string()) == 10

    # Tests that the generated string contains only digits
    def test_only_digits(self):
        number_string = generate_random_number_string()
        assert number_string.isdigit(), 'Generated string contains non-digit characters'

    # Tests that the function 'generate_random_number_string' returns a unique string on each call
    def test_unique_string_on_each_call(self):
        string1 = generate_random_number_string()
        string2 = generate_random_number_string()
        assert string1 != string2

    # Tests that an exception is raised when invalid input is provided
    def test_invalid_input_exception(self):
        with pytest.raises(Exception):
            generate_random_number_string('invalid input')

class UserTestCase(TestCase):



    # Tests that an error is raised when creating a superuser with an empty firstname
    def test_create_superuser_empty_firstname(self):
        with pytest.raises(ValueError):
            UserManager().create_superuser(firstname='', lastname='Doe', password='password', account_number='1234567890')

    # Tests that an error is raised when creating a user with an empty lastname
    def test_create_user_empty_lastname(self):
        with pytest.raises(ValueError):
            UserManager().create_user(firstname='John', lastname='', password='password', account_number='1234567890')

    # Tests that create_user method raises an IntegrityError when creating a user with an existing account number
    def test_create_user_duplicate_account_number(self):
        with pytest.raises(IntegrityError):
            User.objects.create_user(firstname='John', lastname='Doe', password='password', account_number='1234567890')
            User.objects.create_user(firstname='Jane', lastname='Doe', password='password', account_number='1234567890')