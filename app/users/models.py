from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator , MinValueValidator , MaxValueValidator
from utils.helper import get_expiration_time , generate_code
from app.base.models import Organization
from .managers import CustomUserManager
from django.utils import timezone
from app.base.models import OrganizationType , Organization

# # Create your models here.



class CustomUser(AbstractUser):

    class UserType(models.TextChoices):
        CLIENT = 'CLIENT'
        SHAREEK = 'SHAREEK'
        ADMIN = 'ADMIN'
    username = None
    first_name = None
    last_name = None
    phonenumber = models.CharField(db_index=True ,max_length=20, validators=[RegexValidator(regex=r'^\d{7,20}$',message='Phone number must be between 7 and 20 digits.',code='invalid_phone')], unique=True, verbose_name='الهاتف')
    fullName = models.CharField(max_length=255 , null=True , blank=True, verbose_name='الاسم')
    email = models.EmailField(unique=True , null=True , blank=True, verbose_name='البريد الالكتروني')
    image = models.ImageField(upload_to='media/images/users/', default='media/images/users/placeholder.jpg')
    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.CLIENT)
    get_notifications = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, verbose_name="مفعل")   

    objects = CustomUserManager()
    USERNAME_FIELD = 'phonenumber'

    def save(self , *args , **kwargs) -> None:
        OTPCode.objects.create( ## put in the save method in CustomUser Model
            phonenumber=self.phonenumber,
            fullName=self.fullName,
            code_type='SIGNUP'
        )
        return super().save(*args, **kwargs)   

    def __str__(self) -> str:
        return f"{self.fullName} - {self.phonenumber}"




class OTPCode(models.Model):
    class CodeTypes(models.TextChoices):
        SIGNUP = 'SIGNUP'
        RESET_PASSWORD = 'RESET_PASSWORD'
        FORGET_PASSWORD = 'FORGET_PASSWORD'

    phonenumber = models.CharField(max_length=20)
    fullName = models.CharField(max_length=40 , null=True , blank=True)
    code = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)] , default=generate_code)
    createdAt = models.DateTimeField(auto_now_add=True)
    expiresAt = models.DateTimeField(default=get_expiration_time)
    code_type = models.CharField(max_length=20, choices=CodeTypes.choices , default=CodeTypes.SIGNUP)
    is_used = models.BooleanField(default=False)

    def checkLimit(phonenumber):
        return OTPCode.objects.filter(phonenumber=phonenumber,createdAt__gt=timezone.localtime()-timezone.timedelta(minutes=15)).count() >= 5 

    def __str__(self) -> str:
        return f"{self.phonenumber} - {self.code}"



class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.user.fullName   
    


class Shareek(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    job = models.CharField(max_length=255)

    def create_organization(commercial_register_id ,organization_type ,organization_name ,**args):
        organization_type = OrganizationType.objects.get(id=organization_type)
        organization = Organization.objects.create(
            name=organization_name,
            organization_type=organization_type,
            commercial_register_id=commercial_register_id
        )
        return organization

    def __str__(self) -> str:
        return f"{self.user.fullName} - {self.user.id}"


class Subscription(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    days = models.IntegerField(validators=[MinValueValidator(1)])




class SupportChat(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.fullName} - {self.id}"


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat = models.ForeignKey(SupportChat, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)





class Notification(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title




class UserNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)



class Report(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.fullName} - {self.organization}"


