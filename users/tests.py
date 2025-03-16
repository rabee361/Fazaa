from rest_framework.test import APITestCase
from utils.test import create_client , create_shareek
from users.models import OTPCode
from utils.types import CodeTypes
# Create your tests here.





class AuthenticationTestCase(APITestCase):
    def setUp(self):
       self.client_refresh_token = ''
       self.shareek_refresh_token = ''
       self.client_access_token = ''
       self.shareek_access_token = ''
       self.client_id = ''
       self.shareek_id = ''

    def test_signup_shareek(self):
        data={
            'phonenumber': '0554455345',
            'password':'shareek123@@',
            'password2':'shareek123@@'
        }   
        response = self.client.post('/api/auth/shareek/sign-up/',data, format='json')
        self.shareek_id = response.data['id']
        self.shareek_refresh_token = response.json()['tokens']['refresh']
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/api/auth/shareek/token/refresh/',{'refresh':self.shareek_refresh_token} , format='json')
        self.assertEqual(response.status_code, 200)
        self.shareek_access_token = response.json()['access']

        sahreek_data = {
            'email': 'test@gmail.com',
            'full_name': 'test',
            # 'image': 'test.com',
            'organization_name': 'test',
            'organization_type': 1,
            'job': 'manager',
            'commercial_register_id': 234324223
        }

        response = self.client.post('/api/auth/shareek/register-shareek/', data=sahreek_data, format='json')
        self.assertEqual(response.status_code , 200)
        response = self.client.get('/api/auth/shareek/notifications/' , headers={'Authorization':f'Bearer {self.shareek_access_token}'} , format='json')
        self.assertEqual(response.status_code , 200)
        response = self.client.post(f'/api/auth/shareek/activate-notifications/{self.shareek_id}/')
        self.assertEqual(response.status_code , 200)
        repsonse = self.client.post(f'/api/auth/shareek/logout/' , headers={'Authorization':f'Bearer {self.shareek_access_token}'}, format='json')
        # response = self.client.delete(f'/api/auth/shareek/delete/', headers={'Authorization':f'Bearer {self.shareek_access_token}'}, format='json')
        # self.assertEqual(response.status_code, 200)

    def test_signup_client(self):
        data = {
            'phonenumber': '0554455346',
            'password':'client123@@',
            'password2':'client123@@'
        }
        response = self.client.post('/api/auth/client/sign-up/',data, format='json')
        self.client_id = response.data['id']
        self.assertEqual(response.status_code, 200)
        self.client_refresh_token = response.json()['tokens']['refresh']
        response = self.client.post('/api/auth/client/token/refresh/',{'refresh':self.client_refresh_token} , format='json')
        self.assertEqual(response.status_code, 200)
        self.client_access_token = response.json()['access']
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/auth/client/notifications/' , headers={'Authorization':f'Bearer {self.client_access_token}'} , format='json')
        self.assertEqual(response.status_code , 200)
        response = self.client.post(f'/api/auth/client/activate-notifications/{self.client_id}/')
        self.assertEqual(response.status_code , 200)
        repsonse = self.client.post(f'/api/auth/client/logout/' , headers={'Authorization':f'Bearer {self.client_access_token}'}, format='json')
        response = self.client.delete(f'/api/auth/client/delete/', headers={'Authorization':f'Bearer {self.client_access_token}'}, format='json')




class LoginTestCase(APITestCase):
    def setUp(self):
       self.shareek_user = create_shareek()
       self.client_user = create_client()

    def test_login_shareek(self):
        data={
            'phonenumber':self.shareek_user.phonenumber,
            'password':'shareek123@@'
        }
        response = self.client.post('/api/auth/shareek/login/',data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_login_client(self):
        data={
            'phonenumber':self.client_user.phonenumber,
            'password':'client123@@'
        }
        response = self.client.post('/api/auth/client/login/',data , format='json')
        self.assertEqual(response.status_code, 200)




class TestOTP(APITestCase):
    def setUp(self):
        self.client_user = create_client()
        self.shareek_user = create_shareek()

    def test_otp_signup_client(self):
        response = self.client.post('/api/auth/client/signup-otp/',{'phonenumber':self.client_user.phonenumber}, format='json')
        code = OTPCode.objects.get(phonenumber=self.client_user.phonenumber, code_type=CodeTypes.SIGNUP).code
        code_verification = self.client.post('/api/auth/client/verify-otp/',{'code':code}, format='json')
        self.assertEqual(code_verification.status_code, 200)

    def test_otp_forget_password_client(self):
        response = self.client.post('/api/auth/client/forget-password-otp/',{'phonenumber':self.client_user.phonenumber}, format='json')
        code = OTPCode.objects.get(phonenumber=self.client_user.phonenumber, code_type=CodeTypes.FORGET_PASSWORD).code
        code_verification = self.client.post('/api/auth/client/verify-otp/',{'code':code}, format='json')
        self.assertEqual(code_verification.status_code, 200)

    def test_otp_reset_password_client(self):
        response = self.client.post('/api/auth/client/reset-password-otp/',{'phonenumber':self.client_user.phonenumber}, format='json')
        code = OTPCode.objects.get(phonenumber=self.client_user.phonenumber , code_type=CodeTypes.RESET_PASSWORD ).code
        code_verification = self.client.post('/api/auth/client/verify-otp/',{'code':code}, format='json')
        self.assertEqual(code_verification.status_code, 200)

    def test_otp_signup_shareek(self):
        response = self.client.post('/api/auth/shareek/signup-otp/',{'phonenumber':self.shareek_user.phonenumber}, format='json')
        code = OTPCode.objects.get(phonenumber=self.shareek_user.phonenumber, code_type=CodeTypes.SIGNUP ).code
        code_verification = self.client.post('/api/auth/shareek/verify-otp/',{'code':code}, format='json')
        self.assertEqual(code_verification.status_code, 200)

    def test_otp_forget_password_shareek(self):
        response = self.client.post('/api/auth/shareek/forget-password-otp/',{'phonenumber':self.shareek_user.phonenumber}, format='json')
        code = OTPCode.objects.get(phonenumber=self.shareek_user.phonenumber, code_type=CodeTypes.FORGET_PASSWORD).code
        code_verification = self.client.post('/api/auth/shareek/verify-otp/',{'code':code}, format='json')
        self.assertEqual(code_verification.status_code, 200)

    def test_otp_reset_password_shareek(self):
        response = self.client.post('/api/auth/shareek/reset-password-otp/',{'phonenumber':self.shareek_user.phonenumber}, format='json')
        code = OTPCode.objects.get(phonenumber=self.shareek_user.phonenumber , code_type=CodeTypes.RESET_PASSWORD).code
        code_verification = self.client.post('/api/auth/shareek/verify-otp/',{'code':code}, format='json')
        self.assertEqual(code_verification.status_code, 200)


