from django.db import models

class DeliveryCompanyUrlManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def delete_delivery_urls(self, ids=None):
        if ids:
            queryset = self.get_queryset().filter(id__in=ids)
            return queryset.update(deleted=True, active=False, url=None)
        else:
            return self.get_queryset().update(deleted=True, active=False, url=None)


class SocialMediaUrlManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def delete_social_urls(self, ids=None):
        if ids:
            queryset = self.get_queryset().filter(id__in=ids)
            return queryset.update(deleted=True, active=False, url=None)
        else:
            return self.get_queryset().update(deleted=True, active=False, url=None)

