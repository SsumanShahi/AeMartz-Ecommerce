from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',show_products),
    path('about/',AboutUs),
    path('contact/',ContactUs),
    path('tracker/',TrackingStatus),
    path('search/',Search ),
    path('products/<int:myid>',Productview ),
    path('checkout/',Checkout ),



]
