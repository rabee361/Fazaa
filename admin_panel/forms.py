from django import forms
from django.core.validators import RegexValidator
from users.models import Shareek, User, Organization, OrganizationType, Notification
from base.models import SocialMedia, DeliveryCompany, Catalog, ClientOffer , ServiceOffer, Branch
from django.db import transaction
from django.contrib.gis.geos import Point

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), 
        required=True,
        label="كلمة المرور"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=True, 
        label='تأكيد كلمة المرور'
    )
    phonenumber = forms.CharField(
        validators=[RegexValidator(r'^\d{7,20}$', message='يجب أن يحتوي رقم الهاتف على أرقام فقط وأن يكون طوله بين 7 و 20 رقم')],
        label='رقم الهاتف'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autocomplete': 'off'}),
        required=False,
        label='البريد الالكتروني'
    )

    class Meta:
        model = User
        fields = ['full_name','phonenumber','email','password','confirm_password','image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'size'):
            if image.size > 2 * 1024 * 1024:  # 2MB in bytes
                raise forms.ValidationError('حجم الصورة يجب أن لا يتجاوز 2 ميجابايت')
        return image

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('password', "كلمتا المرور غير متطابقتين")
        return cleaned_data


class ChangePasswordForm(forms.Form):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        required=True, 
        label='كلمة المرور الجديدة'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        required=True, 
        label='تأكيد كلمة المرور الجديدة'
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')

        if not password1 or not password2:
            raise forms.ValidationError('جميع الحقول مطلوبة')

        if password1 != password2:
            raise forms.ValidationError('كلمات المرور غير متطابقة')

        if len(password1) < 8:
            raise forms.ValidationError('كلمة المرور يجب أن تكون أكثر من 8 أحرف')

        return cleaned_data


class UpdateUserForm(UserForm):
    class Meta:
        model = User
        fields = ['full_name','phonenumber','email','image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'size'):
            if image.size > 2 * 1024 * 1024:  # 2MB in bytes
                raise forms.ValidationError('حجم الصورة يجب أن لا يتجاوز 2 ميجابايت')
        return image


class ShareekForm(UserForm):
    job = forms.CharField(max_length=255, required=True, label='الوظيفة')
    organization_type = forms.ModelChoiceField(queryset=OrganizationType.objects.all(), required=True, label='نوع المنظمة')
    organization_name = forms.CharField(max_length=255, required=True, label='اسم المنظمة')

    @transaction.atomic
    def save(self):
        user = super().save()
        user.user_type = 'SHAREEK'
        user.save()
        organization = Organization.objects.create(
            name=self.cleaned_data['organization_name'],
            organization_type=OrganizationType.objects.get(id=self.cleaned_data['organization_type'].id),
        )
        shareek = Shareek.objects.create(
            user=user,
            job=self.cleaned_data['job'],
            organization=organization,
        )
        return shareek

class AdminForm(UserForm):
    class Meta:
        model = User
        fields = ['full_name','phonenumber','email','password','confirm_password','image']

    
class ClientForm(UserForm):
    class Meta:
        model = User
        fields = ['full_name','phonenumber','email','password','confirm_password','image']


class OrganizationInfoForm(forms.ModelForm):    
    class Meta:
        model = Organization
        fields = ['name','description','organization_type','logo','commercial_register_id','website']

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo and hasattr(logo, 'size'):
            if logo.size > 2 * 1024 * 1024:  # 2MB in bytes
                raise forms.ValidationError('حجم الشعار يجب أن لا يتجاوز 2 ميجابايت')
        return logo


class SocialMediaForm(forms.ModelForm):    
    class Meta: 
        model = SocialMedia
        fields = ['name','icon']

    def clean_icon(self):
        icon = self.cleaned_data.get('icon')
        if icon and hasattr(icon, 'size'):
            if icon.size > 2 * 1024 * 1024:  # 2MB in bytes
                raise forms.ValidationError('حجم الشعالأيقونةار يجب أن لا يتجاوز 2 ميجابايت')
        return icon


class DeliveryCompanyForm(forms.ModelForm):    
    class Meta:
        model = DeliveryCompany
        fields = ['name','icon']

    def clean_icon(self):
        icon = self.cleaned_data.get('icon')
        if icon and hasattr(icon, 'size'):
            if icon.size > 2 * 1024 * 1024:  # 2MB in bytes
                raise forms.ValidationError('حجم الأيقونة يجب أن لا يتجاوز 2 ميجابايت')
        return icon



class CatalogForm(forms.ModelForm):    
    class Meta:
        model = Catalog
        fields = ['file','organization','catalog_type']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file and hasattr(file, 'size'):
            if file.size > 10 * 1024 * 1024:  # 2MB in bytes
                raise forms.ValidationError('حجم الملف يجب أن لا يتجاوز 10   0 ميجابايت')
        return file





class UpdateAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name','phonenumber','email','image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'size'):
            if image.size > 2 * 1024 * 1024:  # 2MB in bytes
                raise forms.ValidationError('حجم الصورة يجب أن لا يتجاوز 2 ميجابايت')
        return image



class UpdateShareekForm(forms.ModelForm):
    job = forms.CharField(max_length=255, required=True, label='الوظيفة')
    organization_type = forms.ModelChoiceField(queryset=OrganizationType.objects.all(), required=True, label='نوع المنظمة')
    organization_name = forms.CharField(max_length=255, required=True, label='اسم المنظمة')

    class Meta:
        model = User
        fields = ['full_name','phonenumber','email','image', 'job','organization_type','organization_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
                shareek = Shareek.objects.get(user=self.instance, user__is_deleted=False)
                self.fields['job'].initial = shareek.job
                self.fields['organization_name'].initial = shareek.organization.name
                self.fields['organization_type'].initial = shareek.organization.organization_type
            except Shareek.DoesNotExist:
                pass

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'size'):
            if image.size > 2 * 1024 * 1024:  # 2MB in bytes
                raise forms.ValidationError('حجم الصورة يجب أن لا يتجاوز 2 ميجابايت')
        return image
    
    def save(self):
        user = super().save()
        shareek = Shareek.objects.get(
            user=user,
        )

        if shareek:
            organization = Organization.objects.get(id = shareek.organization.id)
            shareek.job = self.cleaned_data['job']
            shareek.organization = organization
            shareek.save()

            organization.name = self.cleaned_data['organization_name']
            organization.organization_type = OrganizationType.objects.get(id=self.cleaned_data['organization_type'].id)
            organization.save()

        return shareek


class UpdateClientForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name','phonenumber','email','image','is_active']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'size'):
            if image.size > 2 * 1024 * 1024:  # 2MB in bytes
                raise forms.ValidationError('حجم الصورة يجب أن لا يتجاوز 2 ميجابايت')
        return image


class ClientOfferForm(forms.ModelForm):
    class Meta:
        model = ClientOffer
        fields = ['content', 'expiresAt', 'organization', 'template','cover']
        widgets = {
            'expiresAt': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            )
        }
        labels = {
            'content': 'المحتوى',
            'expiresAt': 'تاريخ الانتهاء',
            'organization': 'المنظمة',
            'template': 'القالب'
        }

    def clean_cover(self):
        cover = self.cleaned_data.get('cover')
        if cover and hasattr(cover, 'size'):
            if cover.size > 1 * 1024 * 1024:  # 1MB in bytes
                raise forms.ValidationError('حجم الصورة يجب أن لا يتجاوز 1 ميجابايت')
        return cover
    

class ServiceOfferForm(forms.ModelForm):
    class Meta:
        model = ServiceOffer
        fields = ['content', 'expiresAt', 'organization','organizations']
        widgets = {
            'expiresAt': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
            'organizations': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                }
            )
        }
        labels = {
            'content': 'المحتوى',
            'expiresAt': 'تاريخ الانتهاء',
            'organization': 'المنظمة',
            'organizations': 'المنظمات',
        }


class NotificationForm(forms.ModelForm):
    RECIPIENT_CHOICES = [
        ('all', 'الجميع'),
        ('clients', 'العملاء'),
        ('shareeks', 'الشركاء'),
    ]
    recipient_type = forms.ChoiceField(choices=RECIPIENT_CHOICES, label='المستلمون')

    class Meta:
        model = Notification
        fields = ['title','body','recipient_type']


class BranchForm(forms.ModelForm):
    longitude = forms.FloatField(label='الطول')
    latitude = forms.FloatField(label='العرض')
    
    class Meta:
        model = Branch
        fields = ['description', 'organization', 'name', 'longitude', 'latitude']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.location:
            self.fields['longitude'].initial = self.instance.location.x
            self.fields['latitude'].initial = self.instance.location.y

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.location = Point(
            float(self.cleaned_data['longitude']), 
            float(self.cleaned_data['latitude'])
        )
        if commit:
            instance.save()
        return instance
