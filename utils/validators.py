from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from app.users.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from app.users.models import OrganizationType

def validate_phone_format(value):
    try:
        RegexValidator(regex=r'^\d{7,20}$')(value)
    except ValidationError:
        raise ValidationError("رقم الهاتف يجب أن يكون بين 7 و 20 رقماً")
    return value

def validate_phone_unique(value):
    if CustomUser.objects.filter(phonenumber=value).exists():
        raise ValidationError("يوجد حساب بهذا الرقم , الرجاء استخدام رقم اخر")
    return value

def validate_password_match(password1, password2):
    if password1 != password2:
        raise ValidationError("كلمات المرور غير متطابقة")
    return True

def validate_password_strength(password):
    try:
        validate_password(password)
    except ValidationError:
        raise ValidationError("كلمة المرور يجب أن تكون أكثر من 8 أحرف و تحوي رموز و أرقام")
    return password

def validate_required_field(value, field_name):
    if not value or len(str(value).strip()) == 0:
        raise ValidationError(f"{field_name} مطلوب")
    return value

def validate_organizzation_type(type_id):
    try:
        OrganizationType.objects.get(id=type_id)
    except OrganizationType.DoesNotExist:
        raise ValidationError("نوع المنظمة غير موجود")
    return type_id

