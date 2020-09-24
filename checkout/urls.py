
from django.contrib import admin
from django.urls import path
from checkout.views import checkout,checkout_success

urlpatterns = [

    path('<str:type>/',checkout,name='checkout'),
    path('checkout_success/<order_number>', checkout_success, name='checkout_success'),
    #path('cache_checkout_data/', cache_checkout_data, name='cache_checkout_data'),
    #path('wh/', webhook, name='webhook'),


]
