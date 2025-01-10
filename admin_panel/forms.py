from django import forms
from django.core.validators import RegexValidator
from users.models import Shareek, User, Organization, OrganizationType
from base.models import SocialMedia, DeliveryCompany, Catalog



class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='تأكيد كلمة المرور')
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
            raise forms.ValidationError('كلمة المرور غير متطابقة')
        return cleaned_data


class ShareekForm(UserForm):
    job = forms.CharField(max_length=255, required=True, label='الوظيفة')
    organization_type = forms.ModelChoiceField(queryset=OrganizationType.objects.all(), required=True, label='نوع المنظمة')
    organization_name = forms.CharField(max_length=255, required=True, label='اسم المنظمة')

    def save(self):
        user =  super().save()
        user.user_type = 'SHAREEK'
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


class SocialMediaform(forms.ModelForm):    
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
