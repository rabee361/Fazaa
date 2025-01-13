from django.test import TestCase
from rest_framework.test import APITestCase
from utils.test import create_client , create_shareek
from users.models import User
from users.serializers import UserSerializer
# Create your tests here.





class SignUpShareekTestCase(APITestCase):
    def setUp(self):
       self.clientUser= create_shareek()

    def test_signup_shareek(self):
        data={
            'phonenumber': '0554455345',
            'password':'shareek123@@',
            'password2':'shareek123@@'
        }   
        response = self.client.post('/api/auth/shareek/sign-up/',data)
        self.assertEqual(response.status_code, 200)



class LoginShareekTestCase(APITestCase):
    def setUp(self):
       self.clientUser= create_shareek()

    def test_signup_shareek(self):
        data={
            'phonenumber':self.clientUser.phonenumber,
            'password':'shareek123@@'
        }
        response = self.client.post('/api/auth/shareek/login/',data)
        self.assertEqual(response.status_code, 200)


 
class SignUpClientTestCase(APITestCase):
    def setUp(self):
       self.clientUser= create_client()

    def test_signup_client(self):
        data = {
            'phonenumber': '0554455345',
            'password':'client123@@',
            'password2':'client123@@'
        }
        response = self.client.post('/api/auth/client/sign-up/',data)
        self.assertEqual(response.status_code, 200)



class LoginClientTestCase(APITestCase):
    def setUp(self):
       self.clientUser= create_client()

    def test_login_client(self):
        data={
            'phonenumber':self.clientUser.phonenumber,
            'password':'client123@@'
        }
        response = self.client.post('/api/auth/client/login/',data)
        self.assertEqual(response.status_code, 200)


# class ListOrganizationTestCase(APITestCase):
#     def setUp(self):
#        self.clientUser= create_client()

#     def test_get_services(self):
#         # auth client user
#         self.client.force_authenticate(user=self.clientUser)
#         response = self.client.post('/service/client/get_services')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['isSuccess'],True)
#         self.assertEqual(len(response.json()['data']),Service.objects.all().count())
#         self.assertEqual(response.json()['data'],ServiceSerializer(Service.objects.all(),many=True).data)


# class OrderConfigTestCase(APITestCase):
#     def  setUp(self):
#        self.clientUser= create_client()
#     def test_get_order_config(self):
#         # auth client user
#         self.client.force_authenticate(user=self.clientUser)
#         response = self.client.get('/auth/client/app_config')
#         self.assertEqual(response.status_code, 200)