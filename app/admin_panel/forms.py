from django import forms
from django.core.validators import RegexValidator
from app.users.models import Shareek , CustomUser , Organization , OrganizationType



class ShareekForm(forms.Form):
    job = forms.CharField(max_length=255, required=True, label='الوظيفة')
    organization_type = forms.ModelChoiceField(queryset=OrganizationType.objects.all(), required=True, label='نوع المنظمة')
    fullName = forms.CharField(max_length=255, required=True, label='الاسم')
    phonenumber = forms.CharField(max_length=20, validators=[RegexValidator(regex=r'^\d{7,20}$',message='Phone number must be between 7 and 20 digits.',code='invalid_phone')], required=True, label='الهاتف')
    email = forms.EmailField(required=False, label='البريد الالكتروني')
    get_notifications = forms.BooleanField(required=False, label='تلقي الإشعارات')
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label='كلمة المرور')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='تأكيد كلمة المرور')
    organization_name = forms.CharField(max_length=255, required=True, label='اسم المنظمة')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('كلمة المرور غير متطابقة')
        return cleaned_data

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            fullName=self.cleaned_data['fullName'],
            phonenumber=self.cleaned_data['phonenumber'],
            email=self.cleaned_data['email'],
            get_notifications=self.cleaned_data['get_notifications'],
            password=self.cleaned_data['password'],
        )
        organization = Organization.objects.create(
            organization_name=self.cleaned_data['organization_name'],
            organization_type=OrganizationType.objects.get(id=self.cleaned_data['organization_type']),
        )
        shareek = Shareek.objects.create(
            user=user,
            job=self.cleaned_data['job'],
            organization=organization,
        )
        return shareek
