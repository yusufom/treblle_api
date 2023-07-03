import random

def generate_random_number_string():
    number_string = ""
    for _ in range(10):
        digit = random.randint(0, 9)
        number_string += str(digit)
    return number_string

account_number = generate_random_number_string()