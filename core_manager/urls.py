from core_manager.views.borrowing import BorrowingViewSet
from rest_framework import routers
from django.urls import path, include
from core_manager.views.library import LibraryViewSet
from core_manager.views.author import AuthorView
from core_manager.views.book import BookViewSet

router = routers.DefaultRouter()
router.register(r'libraries', LibraryViewSet, basename='library')
router.register(r'authors', AuthorView, basename='author')
router.register(r'books', BookViewSet, basename='book')
router.register(r'borrowings', BorrowingViewSet, basename='borrowing')

urlpatterns = [
    path('', include(router.urls)),    
] 
