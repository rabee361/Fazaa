from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from base.models import Organization
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse


class OrganizationCheckMixin:
    """
    Mixin that provides a method to check if an organization exists and is not deleted.
    """
    def get_organization(self, id):
        """
        Retrieves an organization by ID, ensuring it exists and is not deleted.
        Raises NotFound if the organization doesn't exist or is deleted.
        """
        try:
            return Organization.objects.prefetch_related('branch_set').get(id=id)
        except Organization.DoesNotExist:
            raise NotFound({'error': 'لا يوجد منظمة بهذا الرقم'})



class CustomLoginRequiredMixin(LoginRequiredMixin):
    """
    Custom login required mixin that redirects to the named 'login' URL
    """

    def get_login_url(self):
        """
        Return the URL to redirect to when login is required.
        Uses reverse('login') to get the login URL dynamically.
        """
        return reverse('login')


class AdminLoginRequiredMixin(UserPassesTestMixin):
    """
    Mixin that requires user to be authenticated and have ADMIN user_type.
    Redirects to login page if not authenticated or not an admin.
    """

    def test_func(self):
        """
        Test if user is authenticated and is an admin
        """
        return (
            self.request.user.is_authenticated and
            hasattr(self.request.user, 'user_type') and
            self.request.user.user_type == 'ADMIN'
        )

    def get_login_url(self):
        """
        Return the URL to redirect to when login is required.
        Uses reverse('login') to get the login URL dynamically.
        """
        return reverse('login')