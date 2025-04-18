from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from base.models import Organization

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
