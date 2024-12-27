from datetime import timedelta
from django.utils import timezone
import random

def get_expiration_time():
    return timezone.now() + timedelta(minutes=10)

def generate_code():
    code = random.randint(1000,9999)
    return code

def generateShortUrl():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    random_string = ''.join(random.choice(letters) for _ in range(8))
    return random_string