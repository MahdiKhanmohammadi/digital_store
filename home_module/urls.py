from django.urls import path
from .views import home,search_product

urlpatterns = [
    path('',home,name='home'),
    path('index',home),
    path('home',home),
    path('search',search_product,name='search_products')
]