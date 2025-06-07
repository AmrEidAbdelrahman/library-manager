from django.db import models
from django.utils.translation import gettext_lazy as _
from .library import Library
from .author import Author
from .category import Category

class Book(models.Model):
    title = models.CharField(_('title'), max_length=255)
    isbn = models.CharField(_('ISBN'), max_length=13, unique=True)
    description = models.TextField(_('description'), blank=True)
    publication_date = models.DateField(_('publication date'), null=True, blank=True)
    publisher = models.CharField(_('publisher'), max_length=255, blank=True)
    language = models.CharField(_('language'), max_length=50, blank=True)
    pages = models.PositiveIntegerField(_('pages'), null=True, blank=True)
    cover_image = models.ImageField(_('cover image'), upload_to='book_covers/', null=True, blank=True)
    
    # Relationships
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='books')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    
    # Availability
    total_copies = models.PositiveIntegerField(_('total copies'), default=1)
    available_copies = models.PositiveIntegerField(_('available copies'), default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['isbn']),
        ]

    def __str__(self):
        return self.title

    def is_available(self):
        return self.available_copies > 0 
