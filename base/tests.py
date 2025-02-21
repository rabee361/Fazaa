from rest_framework.test import APIRequestFactory
from utils.test import create_client, create_shareek
from users.models import OTPCode, Shareek
from base.models import Catalog
from django.core.files.uploadedfile import SimpleUploadedFile
from base.views.shareek import CreateCatalogView
from rest_framework.test import APITestCase
from django.core.files.base import File
# Create your tests here.

class TestOrganizationUploads(APITestCase):
    def setUp(self):
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




