from django.db import models

class DeliveryCompanyUrlManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)
    
    def delete_delivery_url(self, ids=None):
        # For queryset bulk operations
        queryset = self.get_queryset()
        if ids:
            queryset = queryset.filter(id__in=ids)
        return queryset.update(deleted=True, active=False, url=None)


class SocialMediaUrlManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)
    
    def delete_social_url(self, ids=None):
        # For queryset bulk operations
        queryset = self.get_queryset()
        if ids:
            queryset = queryset.filter(id__in=ids)
        return queryset.update(deleted=True, active=False, url=None)

