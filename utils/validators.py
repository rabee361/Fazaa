from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from users.models import OrganizationType
from utils.exception_handlers import ErrorResult

def validate_phone_number(value):
    # Check if value contains only digits
    if not str(value).isdigit():
        raise ErrorResult({"error":"رقم الهاتف يجب أن يحتوي على أرقام فقط"})
        
    # Check length is between 7 and 20 digits
    if not (7 <= len(str(value)) <= 20):
        raise ErrorResult({"error":"رقم الهاتف يجب أن يكون بين 7 و 20 رقماً"})
    
    return value


def validate_phone_format(value):
    try:
        RegexValidator(regex=r'^\d{7,20}$')(value)
    except ValidationError:
        raise ErrorResult({"error":"رقم الهاتف يجب أن يكون بين 7 و 20 رقماً"})
    return value

def validate_password_match(password1, password2):
    if password1 != password2:
        raise ErrorResult({"error":"كلمات المرور غير متطابقة"})
    return True


def validate_password_strength(password):
    try:
        validate_password(password)
    except ValidationError:
        raise ErrorResult({"error":"كلمة المرور يجب أن تكون أكثر من 8 أحرف و تحوي رموز و أرقام"})
    return password


def validate_required_field(value, field_name):
    if not value or len(str(value).strip()) == 0:
        raise ErrorResult({"error":f"{field_name} مطلوب"})
    return value


def validate_organization_type(type_id):
    try:
        OrganizationType.objects.get(id=type_id)
    except OrganizationType.DoesNotExist:
        raise ErrorResult({"error":"نوع المنظمة غير موجود"})
    return type_id

def validate_image_size(image):
    if image and image.size > 2 * 1024 * 1024:  # 2MB in bytes
        raise ErrorResult({"error":"حجم الصورة يجب أن لا يتجاوز 2 ميجابايت"})
    return image

def validate_image_extension(image):
    allowed_image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    if image:
        image_extension = image.name.lower()[image.name.rfind('.'):]
        if image_extension not in allowed_image_extensions:
            raise ErrorResult({"error":"يجب أن تكون الصورة بصيغة صالحة"})
    return image


def validate_video_size(video):
    if video and video.size > 25 * 1024 * 1024:  # 25MB in bytes
        raise ErrorResult({"error":"حجم الفيديو يجب أن لا يتجاوز 25 ميجابايت"})
    return video

def validate_video_extension(file):
    allowed_video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv']
    if file:
        file_extension = file.name.lower()[file.name.rfind('.'):]
        if file_extension not in allowed_video_extensions:
            raise ErrorResult({"error":"يجب أن يكون الملف بصيغة فيديو صالحة"})
    return file


def validate_catalog_size(file):
    if file and file.size > 10 * 1024 * 1024:  # 10MB in bytes
        raise ErrorResult({"error":"حجم الملف يجب أن لا يتجاوز 10 ميجابايت"})
    return file

def validate_catalog_extension(file):
    allowed_catalog_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
    if file:
        file_extension = file.name.lower()[file.name.rfind('.'):]
        if file_extension not in allowed_catalog_extensions:
            raise ErrorResult({"error":"يجب أن يكون الملف بصيغة صالحة"})
    return file



