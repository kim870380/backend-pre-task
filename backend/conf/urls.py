"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.contact.views_page import contact_list_page, contact_create_page, contact_detail_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('contact/', contact_list_page, name='contact_list_page'),
    path('contact/new/', contact_create_page, name='contact_create_page'),
    path('contact/<int:pk>/', contact_detail_page, name='contact_detail_page'),
]

