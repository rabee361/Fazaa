from django.core.management.base import BaseCommand, CommandError
from base.models import OrganizationType, Organization , SocialMedia
from users.models import  Shareek , CustomUser
from django.contrib.auth.models import User
from django.db import transaction


class Command(BaseCommand):
    help = "Populate the database"

    def handle(self, *args, **options):

        with transaction.atomic():
            # Create admin users
            admin1, _ = CustomUser.objects.get_or_create(
                username='admin1',
                phonenumber='1234567890',
                defaults={'is_staff': True, 'password': 'r123@@123'}
            )

            admin2, _ = CustomUser.objects.get_or_create(
                username='admin2',
                phonenumber='0987654321', 
                defaults={'is_staff': True, 'password': 'r123@@123'}
            )

            # Create shareek profiles for admins
            shareek1, _ = Shareek.objects.get_or_create(user=admin1, defaults={'job': 'Administrator'})
            shareek2, _ = Shareek.objects.get_or_create(user=admin2, defaults={'job': 'Administrator'})

            # Create organization types
            org_types = []
            type_names = ['Restaurant', 'Retail', 'Supermarket', 'Mini Market', 'Phone Store']
            
            for type_name in type_names:
                org_type, _ = OrganizationType.objects.get_or_create(name=type_name)
                org_types.append(org_type)

            # Create 2 organizations with different types
            organization1, _ = Organization.objects.get_or_create(
                commercial_register_id=10001,
                defaults={
                    'name': 'Restaurant Organization 1',
                    'description': 'This is a restaurant organization',
                    'organization_type': org_types[0], # Restaurant type
                    'website': 'www.restaurant1.com'
                }
            )

            organization2, _ = Organization.objects.get_or_create(
                commercial_register_id=10002,
                defaults={
                    'name': 'Retail Organization 1',
                    'description': 'This is a retail organization', 
                    'organization_type': org_types[1], # Retail type
                    'website': 'www.retail1.com'
                }
            )

            shareek1.organization = organization1
            shareek2.organization = organization2
            shareek1.save()
            shareek2.save()

            # Create social media for organizations
            facebook, _ = SocialMedia.objects.get_or_create(name='فيسبوك', icon='social_media/facebook.png')
            instagram, _ = SocialMedia.objects.get_or_create(name='انستغرام', icon='social_media/instagram.png')
            telegram, _ = SocialMedia.objects.get_or_create(name='تليجرام', icon='social_media/telegram.png')
            twitter, _ = SocialMedia.objects.get_or_create(name='تويتر', icon='social_media/twitter.png')
            snapchat, _ = SocialMedia.objects.get_or_create(name='سناب شات', icon='social_media/snapchat.png')
            whatsapp, _ = SocialMedia.objects.get_or_create(name='واتساب', icon='social_media/whatsapp.png')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database'))