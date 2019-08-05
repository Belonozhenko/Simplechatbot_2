"""Simplechatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include, url
from . import views as my_view


urlpatterns = [
    path('', my_view.base),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/$', my_view.signup, name='signup'),
 #   url(r'^accounts/login/$', my_view.login, name='login'),
    url(r'^chat/', include('chat.urls'), name='room'),
    path('admin/', admin.site.urls),
    #path('', include('chat.urls'), name='index'),



]
