from django import forms
from django.core.validators import RegexValidator
from app.users.models import Shareek , CustomUser , Organization , OrganizationType
from app.base.models import SocialMedia , DeliveryCompany



class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='تأكيد كلمة المرور')
    class Meta:
        model = CustomUser
        fields = ['full_name','phonenumber','email','password','confirm_password','image']

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
        model = CustomUser
        fields = ['full_name','phonenumber','email','password','confirm_password','image']

    
class ClientForm(UserForm):
    class Meta:
        model = CustomUser
        fields = ['full_name','phonenumber','email','password','confirm_password','image']


class SocialMediaForm(forms.ModelForm):
    icon = forms.ImageField(required=False, label='الصورة')
    class Meta:
        model = SocialMedia
        fields = ['name']


class DeliveryCompanyForm(forms.ModelForm):
    icon = forms.ImageField(required=True, label='الصورة')
    class Meta:
        model = DeliveryCompany
        fields = ['name','icon']

