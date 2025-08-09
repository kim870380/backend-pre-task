from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, LabelViewSet

router = DefaultRouter()
router.register(r'contact', ContactViewSet, basename='contact')
router.register(r'contact-label', LabelViewSet, basename='contact-label')

urlpatterns = [
    path('', include(router.urls)),
]