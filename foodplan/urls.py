"""
URL configuration for foodplan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import os

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from foodplan import settings
from foodplan_site.views import index, free_menus, card

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('free_menus/', free_menus, name='free_menus'),
    path('card/', card, name='card'),
    path('users/', include('users.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
