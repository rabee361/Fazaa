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

def getRandomPhonenumber():
    return '01' + str(random.randint(100000000,999999999))

def getRandomEmail():
    return 'test' + str(random.randint(100000000,999999999)) + '@test.com'

def getRandomPassword():
    return 'rabee123@@123'
