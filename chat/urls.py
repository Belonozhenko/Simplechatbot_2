# chat/urls.py

from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.contrib.auth.views import auth_logout
from . import views

urlpatterns = [
    #url(r'', views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),


]
