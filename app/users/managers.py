from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phonenumber, fullName=None, email=None, password=None,get_notifications=True, **extra_fields):
        if not phonenumber:
            raise ValueError('Users must have a phonenumber')
        user = self.model(phonenumber=phonenumber, email=email, fullName=fullName, get_notifications=get_notifications)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phonenumber, fullName=None, email=None, password=None, **extra_fields):
        user = self.create_user(phonenumber, fullName, email, password)
        user.user_type = 'admin'
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
