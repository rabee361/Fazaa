from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phonenumber, full_name=None, email=None, password=None,get_notifications=True, **extra_fields):
        if not phonenumber:
            raise ValueError('Users must have a phonenumber')
        user = self.model(phonenumber=phonenumber, email=email, full_name=full_name, get_notifications=get_notifications)
        print(password)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phonenumber, full_name=None, email=None, password=None, **extra_fields):
        user = self.create_user(phonenumber, full_name, email, password)
        user.user_type = 'ADMIN'
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
