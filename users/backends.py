from django.contrib.auth.backends import ModelBackend
from users.models import User

class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, phonenumber=None, password=None, **kwargs):
        try:
            user = User.objects.get(phonenumber=phonenumber)
        except User.DoesNotExist:
            return None
        print(user)
        print(password)
        print(user.check_password(password))
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None