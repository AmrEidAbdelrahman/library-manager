from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils.translation import gettext_lazy as _

class Library(models.Model):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    address = models.TextField(_('address'))
    phone = models.CharField(_('phone'), max_length=15)
    email = models.EmailField(_('email'))
    website = models.URLField(_('website'), blank=True)
    location = gis_models.PointField(_('location'), geography=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('library')
        verbose_name_plural = _('libraries')
        ordering = ['name']

    def __str__(self):
        return self.name 
