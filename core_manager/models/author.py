from django.db import models
from django.utils.translation import gettext_lazy as _

class Author(models.Model):
    name = models.CharField(_('name'), max_length=255)
    biography = models.TextField(_('biography'), blank=True)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    death_date = models.DateField(_('death date'), null=True, blank=True)
    nationality = models.CharField(_('nationality'), max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')
        ordering = ['name']

    def __str__(self):
        return self.name 
