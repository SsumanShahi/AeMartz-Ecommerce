from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',blog_index),
    path('blogpost/<int:id>', blogpost),
]
