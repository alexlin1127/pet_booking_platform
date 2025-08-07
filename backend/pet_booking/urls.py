"""
URL configuration for pet_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from pet_booking.stores.views import StoreProfileViewSet, StoreAdminViewSet, StorePostViewSet, AdminPostViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'store/profile', StoreProfileViewSet, basename='store-profile')
router.register(r'admin/stores', StoreAdminViewSet, basename='admin-stores')
router.register(r'store/posts', StorePostViewSet, basename='store-posts')
router.register(r'admin/posts', AdminPostViewSet, basename='admin-posts')


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls))
]
