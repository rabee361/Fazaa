from utils.test import *
from users.models import *
from base.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
# Create your tests here.

class TestOrganizationUploads(APITestCase):
    def setUp(self):
        self.delivery = create_delivery()
        self.social = create_social()
        self.shareek = create_shareek()

    def test_create_catalog(self):
        organization = Shareek.objects.get(id=self.shareek.id).organization
        file = open('test.pdf', 'rb')
        upload_file = SimpleUploadedFile('test.pdf', file.read()) # creating the file
        data = {
            'catalog_type': 'OFFERS',
            'file': upload_file,
            'organization': organization.id
        }
        response = self.client.post('/api/shareek/organization/catalogs/create/', data)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(f'/api/shareek/organization/{organization.id}/catalogs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_social_media(self):
        organization = Shareek.objects.get(id=self.shareek.id).organization
        data = {
            'organization': organization,
            'social_media': self.social,
            'active': True,
            'url': 'https://www.reddit.com/r/django/comments/senayk/continuous_integration_and_deployment_for_django/'
        }
        social_url = SocialMediaUrl.objects.filter(organization=organization).first()
        response = self.client.put(f'/api/shareek/organization/social-urls/{social_url.id}/update/', data)
        self.assertEqual(response.status_code, 200)

    def test_create_delivery_company(self):
        organization = Shareek.objects.get(id=self.shareek.id).organization
        data = {
            'organization': organization,
            'delivery_company': self.delivery,
            'active': True,
            'url': 'https://www.reddit.com/r/django/comments/senayk/continuous_integration_and_deployment_for_django/'
        }
        delivery_url = DeliveryCompanyUrl.objects.filter(organization=organization).first()
        response = self.client.put(f'/api/shareek/organization/delivery-url/{delivery_url.id}/update/', data)
        self.assertEqual(response.status_code, 200)





