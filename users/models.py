from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator , MaxValueValidator , RegexValidator
from utils.helper import get_expiration_time , generate_code
from base.models import Organization
from .managers import UserManager
from django.utils import timezone
from django.db import transaction
from base.models import OrganizationType , Organization
from django.core.exceptions import ValidationError
from utils.types import UserType , CodeTypes

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    phonenumber = models.CharField(
        db_index=True, 
        unique=True,
        max_length=20, 
        verbose_name='الهاتف',
        validators=[RegexValidator(r'^\d{7,20}$', message='يجب أن يحتوي رقم الهاتف على أرقام فقط وأن يكون طوله بين 7 و 20 رقم')],
        null=False,
        blank=False,
        error_messages={
            'unique': 'هذا الرقم مستخدم من قبل'
        }
    )
    full_name = models.CharField(max_length=255 , null=True , blank=True, verbose_name='الاسم')
    email = models.EmailField(null=True , blank=True, verbose_name='البريد الالكتروني')
    image = models.ImageField(upload_to='images/users/', default="images/users/placeholder.jpg" , verbose_name="الصورة الشخصية")
    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.CLIENT)
    get_notifications = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, verbose_name="مفعل")   
    long = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = 'phonenumber'

    def clean(self):
        if self.image and self.image.size > 2 * 1024 * 1024:  # 2MB in bytes
            raise ValidationError('حجم الصورة يجب أن لا يتجاوز 2 ميجابايت')

        if self.image and not self.image.name.endswith(('.jpg', '.jpeg', '.png','webp')):
            raise ValidationError('يجب أن يكون الصورة بصيغة jpg أو jpeg أو png أو webp')

    def create_signup_otp(self, *args, **kwargs):
        code = OTPCode.objects.filter(phonenumber=self.phonenumber, expiresAt__date=timezone.now().date(), is_used=False).first()
        if not code:
            otp = OTPCode.objects.create(
                code_type='SIGNUP',
                phonenumber=self.phonenumber,
                full_name=self.full_name
            )
            return otp.code

    def create_chat(self):
        if not SupportChat.objects.filter(user=self).exists():
            chat = SupportChat.objects.create(
                user=self,
            )
            return chat.id

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return f"{self.full_name} - {self.phonenumber}"



class OTPCode(models.Model):
    phonenumber = models.CharField(max_length=20)
    full_name = models.CharField(max_length=40 , null=True , blank=True)
    code = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)] , default=generate_code)
    createdAt = models.DateTimeField(auto_now_add=True)
    expiresAt = models.DateTimeField(default=get_expiration_time)
    code_type = models.CharField(max_length=20, choices=CodeTypes.choices , default=CodeTypes.SIGNUP)
    is_used = models.BooleanField(default=False)

    @staticmethod
    def checkLimit(phonenumber):
        return OTPCode.objects.filter(phonenumber=phonenumber,createdAt__gt=timezone.localtime()-timezone.timedelta(minutes=15)).count() >= 5 

    def __str__(self) -> str:
        return f"{self.phonenumber} - {self.code}"



class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.user.phonenumber} - {self.user.full_name}" 
    
    class Meta:
        ordering = ['-id']


class Shareek(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True, related_name='shareeks')
    job = models.CharField(max_length=255, null=True, blank=True)

    @transaction.atomic 
    def create_organization(commercial_register_id ,organization_type ,organization_name ,**args):
        organization_type = OrganizationType.objects.get(id=organization_type[0])
        organization = Organization.objects.create(
            name=organization_name[0],
            organization_type=organization_type,
            commercial_register_id=commercial_register_id[0]
        )
        organization.create_social_media()
        organization.create_delivery_company()
        return organization
    
    @transaction.atomic
    def update_organization(self ,commercial_register_id=None ,organization_type=None ,organization_name=None ,job=None ,**args):
        if organization_type is not None:
            self.organization.organization_type = organization_type
        if organization_name is not None:
            self.organization.name = organization_name 
        if commercial_register_id is not None:
            self.organization.commercial_register_id = commercial_register_id
        if job is not None:
            self.job = job
        self.organization.save()
        self.save()
        return self.organization

    def __str__(self) -> str:
        return f"{self.user.full_name} - {self.user.id}"

    class Meta:
        ordering = ['-id']



class SupportChat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.full_name} - {self.id}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(SupportChat, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.sender.full_name} - {self.chat.user.full_name}"




class Notification(models.Model):
    title = models.CharField(max_length=255 , verbose_name='العنوان')
    body = models.CharField(max_length=255 , verbose_name='النص')
    createdAt = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الإنشاء')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-id']



class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.full_name} - {self.title}"

    class Meta:
        ordering = ['-id']
