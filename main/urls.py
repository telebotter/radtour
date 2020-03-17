#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.list, name='main_list'),
    #path('admin/', views.index, name='main_admin'),
    path('touren/', views.list, name='main_list'),
    path('tour/<touralias>', views.tour, name='main_tour'),
    path('tour/<touralias>/edit', views.tour_edit, name='main_tour_edit'),
    path('webodf/', views.webodf, name='web_odf'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/login.html'), name='logout'),
    #path('login/', views.login_view),
    #path('auth/', include('django.contrib.auth.urls')),
    #path('karte/', include('karte.urls')),
    #path('bilder/', include('bilder.urls')),
]
