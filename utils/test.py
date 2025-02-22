from users.models import User, Client  ,Shareek,Organization,OrganizationType
from utils.helper import getRandomPhonenumber, getRandomEmail, getRandomPassword
from django.core.files.uploadedfile import SimpleUploadedFile
from base.models import SocialMedia , DeliveryCompany 


#function to create client user
def create_client():
    user=User.objects.create(phonenumber=getRandomPhonenumber(),full_name='test',user_type='CLIENT',password='client123@@',email=getRandomEmail())
    
    #hash password
    user.set_password(user.password)
    user.save()
    #create client object for this user
    client=Client.objects.create(user=user)
    return user


def create_social():
    file = open('test.png', 'rb')
    upload_icon = SimpleUploadedFile('test.png', file.read()) # creating the file
    social = SocialMedia.objects.create(
        name='test',
        icon=upload_icon
    )
    return social


def create_delivery():
    file = open('test.png', 'rb')
    upload_icon = SimpleUploadedFile('test.png', file.read()) # creating the file
    social = DeliveryCompany.objects.create(
        name='test',
        icon=upload_icon
    )
    return social


#function to create driver user
def create_shareek():
    user=User.objects.create(phonenumber=getRandomPhonenumber(),
                                  full_name='test',
                                  user_type='SHAREEK',
                                  password='shareek123@@',
                                  email=getRandomEmail())
    #hash password
    user.set_password(user.password)
    user.save()

    organization_type=OrganizationType.objects.create(id=1) 

    organization=Organization.objects.create(website='https://www.django-rest-framework.org/api-guide/testing/',organization_type=organization_type,name='test',commercial_register_id=1234567890)
    organization.create_social_media()
    organization.create_delivery_company()

    shareek=Shareek.objects.create(user=user,job='test',organization=organization)
    return user



