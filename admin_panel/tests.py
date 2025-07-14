from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from users.models import User, Shareek, Organization, OrganizationType, SupportChat
from base.models import (
    SocialMedia, DeliveryCompany, Branch, ContactUs, AboutUs,
    Subscription, TermsPrivacy, CommonQuestion
)
from django.contrib.gis.geos import Point
import json


class AdminPanelURLTestCase(TestCase):
    """Test case for all admin panel URLs"""
    def setUp(self):
        """Set up test data"""
        self.client = Client()

        # Create admin user
        self.admin_user = User.objects.create_user(
            phonenumber='0512341234',
            full_name='Admin Test User',
            email='admin@test.com',
            password='testpass123',
            user_type='ADMIN'
        )

        # Create client user
        self.client_user = User.objects.create_user(
            phonenumber='1234567891',
            full_name='Client Test User',
            email='client@test.com',
            password='testpass123',
            user_type='CLIENT'
        )

        # Create organization type
        self.org_type = OrganizationType.objects.create(name='Test Organization Type')

        # # Create organization
        # self.organization = Organization.objects.create(
        #     name='Test Organization',
        #     organization_type=self.org_type,
        #     commercial_register_id=1234567890
        # )

        # Create shareek user
        self.shareek_user = User.objects.create_user(
            phonenumber='1234567892',
            full_name='Shareek Test User',
            email='shareek@test.com',
            password='testpass123',
            user_type='SHAREEK'
        )

        # self.shareek = Shareek.objects.create(
        #     user=self.shareek_user,
        #     organization=self.organization,
        #     job='Test Job'
        # )

        # Create test data for various models
        # self.social_media = SocialMedia.objects.create(name='Facebook')
        # self.delivery_company = DeliveryCompany.objects.create(name='Test Delivery')
        self.subscription = Subscription.objects.create(
            name='Basic Plan',
            days=30,
            price=100.00
        )
        self.contact_us = ContactUs.objects.create(
            name='Phone',
            link='tel:+1234567890'
        )
        self.about_us = AboutUs.objects.create(
            name='About Us',
            link='Test content'
        )
        self.terms = TermsPrivacy.objects.create(
            title='Terms',
            content='Test terms content'
        )
        self.common_question = CommonQuestion.objects.create(
            question='Test Question?',
            answer='Test Answer'
        )

        # Create branch with location
        # self.branch = Branch.objects.create(
        #     organization=self.organization,
        #     name='Test Branch',
        #     location=Point(46.6753, 24.7136),  # Riyadh coordinates
        #     description='Test branch description'
        # )

        # Create support chat
        self.support_chat = SupportChat.objects.create(user=self.client_user)

    def login_admin(self):
        """Helper method to login admin user"""
        self.client.login(phonenumber='0512341234', password='testpass123')

    def test_login_view_get(self):
        """Test login page GET request"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'login')

    def test_login_view_post_valid(self):
        """Test login with valid credentials"""
        response = self.client.post(reverse('login'), {
            'phonenumber': '0512341234',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_login_view_post_invalid(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('login'), {
            'phonenumber': '0512341234',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')

    def test_logout_view(self):
        """Test logout functionality"""
        self.login_admin()
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_dashboard_view(self):
        """Test dashboard access"""
        self.login_admin()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_partial_view(self):
        """Test dashboard partial view"""
        self.login_admin()
        response = self.client.get(reverse('dashboard-partial'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admins')

    def test_clients_list_view(self):
        """Test clients list view"""
        self.login_admin()
        response = self.client.get(reverse('clients'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'clients')

    def test_clients_list_view_with_search(self):
        """Test clients list view with search query"""
        self.login_admin()
        response = self.client.get(reverse('clients'), {'q': 'Client'})
        self.assertEqual(response.status_code, 200)

    def test_add_client_view_get(self):
        """Test add client form GET request"""
        self.login_admin()
        response = self.client.get(reverse('add-client'))
        self.assertEqual(response.status_code, 200)

    def test_add_client_view_post(self):
        """Test add client form POST request"""
        self.login_admin()
        response = self.client.post(reverse('add-client'), {
            'full_name': 'New Client',
            'phonenumber': '1234567893',
            'email': 'newclient@test.com',
            'password': 'newpass123',
            'confirm_password': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(phonenumber='1234567893').exists())

    def test_client_info_view(self):
        """Test client info view"""
        self.login_admin()
        response = self.client.get(reverse('client-info', kwargs={'id': self.client_user.id}))
        self.assertEqual(response.status_code, 200)

    def test_shareeks_list_view(self):
        """Test shareeks list view"""
        self.login_admin()
        response = self.client.get(reverse('shareeks'))
        self.assertEqual(response.status_code, 200)

    def test_add_shareek_view_get(self):
        """Test add shareek form GET request"""
        self.login_admin()
        response = self.client.get(reverse('add-shareek'))
        self.assertEqual(response.status_code, 200)

    # def test_shareek_info_view(self):
    #     """Test shareek info view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('shareek-info', kwargs={'id': self.shareek_user.id}))
    #     self.assertEqual(response.status_code, 200)

    def test_admins_list_view(self):
        """Test admins list view"""
        self.login_admin()
        response = self.client.get(reverse('admins'))
        self.assertEqual(response.status_code, 200)

    def test_add_admin_view_get(self):
        """Test add admin form GET request"""
        self.login_admin()
        response = self.client.get(reverse('add-admin'))
        self.assertEqual(response.status_code, 200)

    def test_add_admin_view_post(self):
        """Test add admin form POST request"""
        self.login_admin()
        response = self.client.post(reverse('add-admin'), {
            'full_name': 'New Admin',
            'phonenumber': '1234567894',
            'email': 'newadmin@test.com',
            'password': 'newpass123',
            'confirm_password': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(phonenumber='1234567894', user_type='ADMIN').exists())

    def test_admin_info_view(self):
        """Test admin info view"""
        self.login_admin()
        response = self.client.get(reverse('admin-info', kwargs={'id': self.admin_user.id}))
        self.assertEqual(response.status_code, 200)

    def test_change_password_view(self):
        """Test change password view"""
        self.login_admin()
        response = self.client.get(reverse('change-password', kwargs={'user_id': self.admin_user.id}))
        self.assertEqual(response.status_code, 200)

    def test_chats_view(self):
        """Test support chats list view"""
        self.login_admin()
        response = self.client.get(reverse('chats'))
        self.assertEqual(response.status_code, 200)

    def test_messages_view(self):
        """Test messages view for a specific chat"""
        self.login_admin()
        response = self.client.get(reverse('messages', kwargs={'chat_id': self.support_chat.id}))
        self.assertEqual(response.status_code, 200)

    def test_organization_types_view(self):
        """Test organization types list view"""
        self.login_admin()
        response = self.client.get(reverse('organization-types'))
        self.assertEqual(response.status_code, 200)

    def test_add_organization_type_view(self):
        """Test add organization type view"""
        self.login_admin()
        response = self.client.get(reverse('add-organization-type'))
        self.assertEqual(response.status_code, 200)

    def test_organization_type_info_view(self):
        """Test organization type info view"""
        self.login_admin()
        response = self.client.get(reverse('organization-type-info', kwargs={'id': self.org_type.id}))
        self.assertEqual(response.status_code, 200)

    def test_organizations_view(self):
        """Test organizations list view"""
        self.login_admin()
        response = self.client.get(reverse('organizations'))
        self.assertEqual(response.status_code, 200)

    # def test_organization_info_view(self):
    #     """Test organization info view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('organization-info', kwargs={'id': self.organization.id}))
    #     self.assertEqual(response.status_code, 200)

    def test_catalogs_view(self):
        """Test catalogs list view"""
        self.login_admin()
        response = self.client.get(reverse('catalogs'))
        self.assertEqual(response.status_code, 200)

    def test_add_catalog_view(self):
        """Test add catalog view"""
        self.login_admin()
        response = self.client.get(reverse('add-catalog'))
        self.assertEqual(response.status_code, 200)

    def test_images_gallery_view(self):
        """Test images gallery view"""
        self.login_admin()
        response = self.client.get(reverse('images-gallery'))
        self.assertEqual(response.status_code, 200)

    def test_add_image_view(self):
        """Test add image view"""
        self.login_admin()
        response = self.client.get(reverse('add-image'))
        self.assertEqual(response.status_code, 200)

    def test_reels_gallery_view(self):
        """Test reels gallery view"""
        self.login_admin()
        response = self.client.get(reverse('reels-gallery'))
        self.assertEqual(response.status_code, 200)

    def test_add_reel_view(self):
        """Test add reel view"""
        self.login_admin()
        response = self.client.get(reverse('add-reel'))
        self.assertEqual(response.status_code, 200)

    def test_social_media_view(self):
        """Test social media list view"""
        self.login_admin()
        response = self.client.get(reverse('social-media'))
        self.assertEqual(response.status_code, 200)

    def test_add_social_media_view(self):
        """Test add social media view"""
        self.login_admin()
        response = self.client.get(reverse('add-social-media'))
        self.assertEqual(response.status_code, 200)

    # def test_social_media_info_view(self):
    #     """Test social media info view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('social-media-info', kwargs={'id': self.social_media.id}))
    #     self.assertEqual(response.status_code, 200)

    def test_delivery_companies_view(self):
        """Test delivery companies list view"""
        self.login_admin()
        response = self.client.get(reverse('delivery-companies'))
        self.assertEqual(response.status_code, 200)

    def test_add_delivery_company_view(self):
        """Test add delivery company view"""
        self.login_admin()
        response = self.client.get(reverse('add-delivery-company'))
        self.assertEqual(response.status_code, 200)

    # def test_delivery_company_info_view(self):
    #     """Test delivery company info view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('delivery-company-info', kwargs={'id': self.delivery_company.id}))
    #     self.assertEqual(response.status_code, 200)

    # def test_client_offers_view(self):
    #     """Test client offers list view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('client-offers'))
    #     self.assertEqual(response.status_code, 200)

    # def test_add_client_offer_view(self):
    #     """Test add client offer view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('add-client-offer'))
    #     self.assertEqual(response.status_code, 200)

    # def test_service_offers_view(self):
    #     """Test service offers list view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('service-offers'))
    #     self.assertEqual(response.status_code, 200)

    # def test_add_service_offer_view(self):
    #     """Test add service offer view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('add-service-offer'))
    #     self.assertEqual(response.status_code, 200)

    # def test_offer_templates_view(self):
    #     """Test offer templates list view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('offer-templates'))
    #     self.assertEqual(response.status_code, 200)

    # def test_add_offer_template_view(self):
    #     """Test add offer template view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('add-offer-template'))
    #     self.assertEqual(response.status_code, 200)

    # def test_delivery_links_view(self):
    #     """Test delivery links list view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('delivery-links'))
    #     self.assertEqual(response.status_code, 200)

    # def test_add_delivery_link_view(self):
    #     """Test add delivery link view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('add-delivery-link'))
    #     self.assertEqual(response.status_code, 200)

    # def test_social_links_view(self):
    #     """Test social links list view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('social-links'))
    #     self.assertEqual(response.status_code, 200)

    # def test_add_social_link_view(self):
    #     """Test add social link view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('add-social-link'))
    #     self.assertEqual(response.status_code, 200)

    # def test_branches_view(self):
    #     """Test branches list view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('branches'))
    #     self.assertEqual(response.status_code, 200)

    # def test_add_branch_view(self):
    #     """Test add branch view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('add-branch'))
    #     self.assertEqual(response.status_code, 200)

    # def test_branch_info_view(self):
    #     """Test branch info view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('branch-info', kwargs={'id': self.branch.id}))
    #     self.assertEqual(response.status_code, 200)

    # def test_contact_us_view(self):
    #     """Test contact us list view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('contact-us'))
    #     self.assertEqual(response.status_code, 200)

    # def test_add_contact_us_view(self):
    #     """Test add contact us view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('add-contact-us'))
    #     self.assertEqual(response.status_code, 200)

    # def test_contact_us_info_view(self):
    #     """Test contact us info view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('contact-us-info', kwargs={'id': self.contact_us.id}))
    #     self.assertEqual(response.status_code, 200)

    # def test_about_us_view(self):
    #     """Test about us list view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('about-us'))
    #     self.assertEqual(response.status_code, 200)

    # def test_add_about_us_view(self):
    #     """Test add about us view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('add-about-us'))
    #     self.assertEqual(response.status_code, 200)

    # def test_about_us_info_view(self):
    #     """Test about us info view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('about-us-info', kwargs={'id': self.about_us.id}))
    #     self.assertEqual(response.status_code, 200)

    # def test_subscriptions_view(self):
    #     """Test subscriptions list view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('subscriptions'))
    #     self.assertEqual(response.status_code, 200)

    # def test_add_subscription_view(self):
    #     """Test add subscription view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('add-subscription'))
    #     self.assertEqual(response.status_code, 200)

    # def test_subscription_info_view(self):
    #     """Test subscription info view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('subscription-info', kwargs={'id': self.subscription.id}))
    #     self.assertEqual(response.status_code, 200)

    # def test_reports_view(self):
    #     """Test reports list view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('reports'))
    #     self.assertEqual(response.status_code, 200)

    # def test_terms_view(self):
    #     """Test terms list view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('terms'))
    #     self.assertEqual(response.status_code, 200)

    # def test_term_info_view(self):
    #     """Test term info view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('term-info', kwargs={'id': self.terms.id}))
    #     self.assertEqual(response.status_code, 200)

    # def test_common_questions_view(self):
    #     """Test common questions list view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('common-questions'))
    #     self.assertEqual(response.status_code, 200)

    # def test_add_common_question_view(self):
    #     """Test add common question view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('add-common-question'))
    #     self.assertEqual(response.status_code, 200)

    # def test_common_question_info_view(self):
    #     """Test common question info view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('common-question-info', kwargs={'id': self.common_question.id}))
    #     self.assertEqual(response.status_code, 200)

    # def test_notifications_view(self):
    #     """Test notifications list view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('notifications'))
    #     self.assertEqual(response.status_code, 200)

    # def test_send_notification_view(self):
    #     """Test send notification view"""
    #     self.login_admin()
    #     response = self.client.get(reverse('send-notification'))
    #     self.assertEqual(response.status_code, 200)

    # # Test bulk action views
    # def test_bulk_action_view_clients(self):
    #     """Test bulk action for clients"""
    #     self.login_admin()
    #     response = self.client.post(reverse('bulk-action'), {
    #         'selected_ids': json.dumps([self.client_user.id]),
    #         'action': 'activate'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_organization_types_bulk_action(self):
    #     """Test organization types bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('organization-types-action'), {
    #         'selected_ids': json.dumps([self.org_type.id]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_catalog_bulk_action(self):
    #     """Test catalog bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('catalog-bulk-action'), {
    #         'selected_ids': json.dumps([]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_image_gallery_bulk_action(self):
    #     """Test image gallery bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('image-gallery-bulk-action'), {
    #         'selected_ids': json.dumps([]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_reel_gallery_bulk_action(self):
    #     """Test reel gallery bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('reel-gallery-bulk-action'), {
    #         'selected_ids': json.dumps([]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_social_media_action(self):
    #     """Test social media bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('social-media-action'), {
    #         'selected_ids': json.dumps([self.social_media.id]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_delivery_company_action(self):
    #     """Test delivery company bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('delivery-company-action'), {
    #         'selected_ids': json.dumps([self.delivery_company.id]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_client_offer_action(self):
    #     """Test client offer bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('client-offer-action'), {
    #         'selected_ids': json.dumps([]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_service_offer_action(self):
    #     """Test service offer bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('service-offer-action'), {
    #         'selected_ids': json.dumps([]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_delivery_bulk_action(self):
    #     """Test delivery links bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('delivery-bulk-action'), {
    #         'selected_ids': json.dumps([]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_social_bulk_action(self):
    #     """Test social links bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('social-bulk-action'), {
    #         'selected_ids': json.dumps([]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_branch_action(self):
    #     """Test branch bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('branch-action'), {
    #         'selected_ids': json.dumps([self.branch.id]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_contact_us_action(self):
    #     """Test contact us bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('contact-us-action'), {
    #         'selected_ids': json.dumps([self.contact_us.id]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_about_us_action(self):
    #     """Test about us bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('about-us-action'), {
    #         'selected_ids': json.dumps([self.about_us.id]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_subscription_action(self):
    #     """Test subscription bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('subscription-action'), {
    #         'selected_ids': json.dumps([self.subscription.id]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_common_question_action(self):
    #     """Test common question bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('common-question-action'), {
    #         'selected_ids': json.dumps([self.common_question.id]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_notification_action(self):
    #     """Test notification bulk action"""
    #     self.login_admin()
    #     response = self.client.post(reverse('notification-action'), {
    #         'selected_ids': json.dumps([]),
    #         'action': 'delete'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # # Test slug-based URLs
    # def test_card_url_view(self):
    #     """Test card URL view with organization slug"""
    #     response = self.client.get(reverse('card-url', kwargs={'slug': self.organization.card_url}))
    #     self.assertEqual(response.status_code, 200)

    # def test_catalog_slug_url_view(self):
    #     """Test catalog slug URL view"""
    #     response = self.client.get(f'/catalog/{self.organization.card_url}/')
    #     self.assertEqual(response.status_code, 200)

    # def test_social_slug_url_view(self):
    #     """Test social media slug URL view"""
    #     response = self.client.get(f'/social/{self.organization.card_url}/')
    #     self.assertEqual(response.status_code, 200)

    # def test_website_slug_url_view(self):
    #     """Test website slug URL view"""
    #     response = self.client.get(f'/website/{self.organization.card_url}/')
    #     self.assertEqual(response.status_code, 200)

    # def test_delivery_slug_url_view(self):
    #     """Test delivery slug URL view"""
    #     response = self.client.get(f'/delivery/{self.organization.card_url}/')
    #     self.assertEqual(response.status_code, 200)

    # def test_branch_slug_url_view(self):
    #     """Test branch slug URL view"""
    #     response = self.client.get(f'/branch/{self.branch.short_url}/')
    #     self.assertEqual(response.status_code, 200)

    # def test_404_view(self):
    #     """Test 404 error page"""
    #     response = self.client.get(reverse('404'))
    #     self.assertEqual(response.status_code, 200)

    # def test_500_view(self):
    #     """Test 500 error page"""
    #     response = self.client.get(reverse('500'))
    #     self.assertEqual(response.status_code, 200)

    # # Test authentication and permissions
    # def test_dashboard_requires_login(self):
    #     """Test that dashboard requires admin login"""
    #     response = self.client.get(reverse('dashboard'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, '/login/?next=/dashboard/')

    # def test_clients_requires_admin_login(self):
    #     """Test that clients view requires admin login"""
    #     response = self.client.get(reverse('clients'))
    #     self.assertEqual(response.status_code, 302)

    # def test_non_admin_cannot_access_dashboard(self):
    #     """Test that non-admin users cannot access dashboard"""
    #     self.client.login(phonenumber='1234567891', password='testpass123')  # Client user
    #     response = self.client.get(reverse('dashboard'))
    #     self.assertEqual(response.status_code, 302)

    # def test_shareek_cannot_access_admin_panel(self):
    #     """Test that shareek users cannot access admin panel"""
    #     self.client.login(phonenumber='1234567892', password='testpass123')  # Shareek user
    #     response = self.client.get(reverse('dashboard'))
    #     self.assertEqual(response.status_code, 302)

    # # Test form validation
    # def test_add_client_invalid_form(self):
    #     """Test add client with invalid form data"""
    #     self.login_admin()
    #     response = self.client.post(reverse('add-client'), {
    #         'full_name': '',  # Missing required field
    #         'phonenumber': 'invalid',  # Invalid phone number
    #         'password': 'short',  # Short password
    #         'confirm_password': 'different'  # Different confirmation
    #     })
    #     self.assertEqual(response.status_code, 200)  # Form should be re-rendered with errors

    # def test_add_admin_password_mismatch(self):
    #     """Test add admin with password mismatch"""
    #     self.login_admin()
    #     response = self.client.post(reverse('add-admin'), {
    #         'full_name': 'Test Admin',
    #         'phonenumber': '1234567895',
    #         'email': 'test@admin.com',
    #         'password': 'password123',
    #         'confirm_password': 'different123'
    #     })
    #     self.assertEqual(response.status_code, 200)  # Form should be re-rendered with errors

    # def test_change_password_valid(self):
    #     """Test change password with valid data"""
    #     self.login_admin()
    #     response = self.client.post(reverse('change-password', kwargs={'user_id': self.admin_user.id}), {
    #         'new_password1': 'newpassword123',
    #         'new_password2': 'newpassword123'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_change_password_invalid(self):
    #     """Test change password with invalid data"""
    #     self.login_admin()
    #     response = self.client.post(reverse('change-password', kwargs={'user_id': self.admin_user.id}), {
    #         'new_password1': 'short',
    #         'new_password2': 'different'
    #     })
    #     self.assertEqual(response.status_code, 200)  # Form should be re-rendered with errors

    # # Test search functionality
    # def test_clients_search_by_name(self):
    #     """Test clients search by name"""
    #     self.login_admin()
    #     response = self.client.get(reverse('clients'), {'q': 'Client Test'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Client Test User')

    # def test_clients_search_by_phone(self):
    #     """Test clients search by phone number"""
    #     self.login_admin()
    #     response = self.client.get(reverse('clients'), {'q': '1234567891'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, '1234567891')

    # def test_organizations_search(self):
    #     """Test organizations search"""
    #     self.login_admin()
    #     response = self.client.get(reverse('organizations'), {'q': 'Test Organization'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Test Organization')

    # def test_organization_types_search(self):
    #     """Test organization types search"""
    #     self.login_admin()
    #     response = self.client.get(reverse('organization-types'), {'q': 'Test'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Test Organization Type')

    # # Test HTMX requests
    # def test_clients_htmx_request(self):
    #     """Test clients view with HTMX request"""
    #     self.login_admin()
    #     response = self.client.get(reverse('clients'), HTTP_HX_REQUEST='true')
    #     self.assertEqual(response.status_code, 200)

    # def test_shareeks_htmx_request(self):
    #     """Test shareeks view with HTMX request"""
    #     self.login_admin()
    #     response = self.client.get(reverse('shareeks'), HTTP_HX_REQUEST='true')
    #     self.assertEqual(response.status_code, 200)

    # def test_admins_htmx_request(self):
    #     """Test admins view with HTMX request"""
    #     self.login_admin()
    #     response = self.client.get(reverse('admins'), HTTP_HX_REQUEST='true')
    #     self.assertEqual(response.status_code, 200)

    # # Test pagination
    # def test_clients_pagination(self):
    #     """Test clients list pagination"""
    #     # Create multiple clients to test pagination
    #     for i in range(15):
    #         User.objects.create_user(
    #             phonenumber=f'123456789{i:02d}',
    #             full_name=f'Client {i}',
    #             password='testpass123',
    #             user_type='CLIENT'
    #         )

    #     self.login_admin()
    #     response = self.client.get(reverse('clients'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'page')  # Check if pagination is present

    # # Test invalid IDs
    # def test_client_info_invalid_id(self):
    #     """Test client info view with invalid ID"""
    #     self.login_admin()
    #     response = self.client.get(reverse('client-info', kwargs={'id': 99999}))
    #     self.assertEqual(response.status_code, 404)

    # def test_shareek_info_invalid_id(self):
    #     """Test shareek info view with invalid ID"""
    #     self.login_admin()
    #     response = self.client.get(reverse('shareek-info', kwargs={'id': 99999}))
    #     self.assertEqual(response.status_code, 404)

    # def test_admin_info_invalid_id(self):
    #     """Test admin info view with invalid ID"""
    #     self.login_admin()
    #     response = self.client.get(reverse('admin-info', kwargs={'id': 99999}))
    #     self.assertEqual(response.status_code, 404)

    # def test_organization_info_invalid_id(self):
    #     """Test organization info view with invalid ID"""
    #     self.login_admin()
    #     response = self.client.get(reverse('organization-info', kwargs={'id': 99999}))
    #     self.assertEqual(response.status_code, 404)

    # # Test POST requests for create views
    # def test_add_organization_type_post(self):
    #     """Test add organization type POST request"""
    #     self.login_admin()
    #     response = self.client.post(reverse('add-organization-type'), {
    #         'name': 'New Organization Type'
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(OrganizationType.objects.filter(name='New Organization Type').exists())

    # def test_add_social_media_post(self):
    #     """Test add social media POST request"""
    #     self.login_admin()
    #     response = self.client.post(reverse('add-social-media'), {
    #         'name': 'Instagram'
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(SocialMedia.objects.filter(name='Instagram').exists())

    # def test_add_delivery_company_post(self):
    #     """Test add delivery company POST request"""
    #     self.login_admin()
    #     response = self.client.post(reverse('add-delivery-company'), {
    #         'name': 'New Delivery Company'
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(DeliveryCompany.objects.filter(name='New Delivery Company').exists())

    # def test_add_subscription_post(self):
    #     """Test add subscription POST request"""
    #     self.login_admin()
    #     response = self.client.post(reverse('add-subscription'), {
    #         'name': 'Premium Plan',
    #         'days': 365,
    #         'price': 500.00
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(Subscription.objects.filter(name='Premium Plan').exists())

    # def test_add_contact_us_post(self):
    #     """Test add contact us POST request"""
    #     self.login_admin()
    #     response = self.client.post(reverse('add-contact-us'), {
    #         'name': 'Email',
    #         'link': 'mailto:test@example.com'
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(ContactUs.objects.filter(name='Email').exists())

    # def test_add_about_us_post(self):
    #     """Test add about us POST request"""
    #     self.login_admin()
    #     response = self.client.post(reverse('add-about-us'), {
    #         'title': 'Our Story',
    #         'content': 'This is our story content'
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(AboutUs.objects.filter(title='Our Story').exists())

    # def test_add_common_question_post(self):
    #     """Test add common question POST request"""
    #     self.login_admin()
    #     response = self.client.post(reverse('add-common-question'), {
    #         'question': 'How to use the app?',
    #         'answer': 'Follow the instructions in the app.'
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(CommonQuestion.objects.filter(question='How to use the app?').exists())

    # def test_send_notification_post(self):
    #     """Test send notification POST request"""
    #     self.login_admin()
    #     response = self.client.post(reverse('send-notification'), {
    #         'title': 'Test Notification',
    #         'body': 'This is a test notification',
    #         'recipient_type': 'all'
    #     })
    #     self.assertEqual(response.status_code, 302)

    # # Test URL name resolution
    # def test_all_url_names_resolve(self):
    #     """Test that all URL names can be resolved"""
    #     url_names = [
    #         'login', 'logout', 'dashboard', 'dashboard-partial',
    #         'clients', 'add-client', 'shareeks', 'add-shareek',
    #         'admins', 'add-admin', 'chats', 'organization-types',
    #         'add-organization-type', 'organizations', 'catalogs',
    #         'add-catalog', 'images-gallery', 'add-image',
    #         'reels-gallery', 'add-reel', 'social-media',
    #         'add-social-media', 'delivery-companies',
    #         'add-delivery-company', 'client-offers',
    #         'add-client-offer', 'service-offers', 'add-service-offer',
    #         'offer-templates', 'add-offer-template', 'delivery-links',
    #         'add-delivery-link', 'social-links', 'add-social-link',
    #         'branches', 'add-branch', 'contact-us', 'add-contact-us',
    #         'about-us', 'add-about-us', 'subscriptions',
    #         'add-subscription', 'reports', 'terms',
    #         'common-questions', 'add-common-question',
    #         'notifications', 'send-notification', '404', '500'
    #     ]

    #     for url_name in url_names:
    #         try:
    #             url = reverse(url_name)
    #             self.assertIsNotNone(url)
    #         except Exception as e:
    #             self.fail(f"URL name '{url_name}' could not be resolved: {e}")

    # def tearDown(self):
    #     """Clean up after tests"""
    #     # Clean up any test data if needed
    #     pass
