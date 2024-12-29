from django.contrib.auth.backends import ModelBackend
from app.users.models import CustomUser

class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, phonenumber=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(phonenumber=phonenumber)
        except CustomUser.DoesNotExist:
            return None
        print(user)
        print(password)
        print(user.check_password(password))
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None