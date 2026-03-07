"""
URL configuration for blog_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from .views import *

urlpatterns = [
    path('add/', add_blog, name='add_blog'),
    path('', blog_list, name='blog_list'),
    path('edit/<int:id>/', edit_blog, name='edit_blog'),
    path('delete/<int:id>/', delete_blog, name='delete_blog'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/', reset_password, name='reset_password'),


]














# from django.urls import path
# from .views import (
#     BlogListView,
#     BlogCreateView,
#     BlogUpdateView,
#     BlogDeleteView
# )

# urlpatterns = [
#     path('', BlogListView.as_view(), name='blog_list'),
#     path('add/', BlogCreateView.as_view(), name='add_blog'),
#     path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit_blog'),
#     path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete_blog'),
# ]
