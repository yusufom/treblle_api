import random


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_random_number_string():
    number_string = ""
    for _ in range(10):
        digit = random.randint(0, 9)
        number_string += str(digit)
    return number_string

account_number = generate_random_number_string()