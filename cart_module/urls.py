from django.urls import path

from cart_module.views import add_product_to_cart,show_cart,remove_product_in_cart,complete_remove,discount_code

urlpatterns = [
    path('add-item',add_product_to_cart,name='add_to_cart'),
    path('remove-item',remove_product_in_cart,name='remove_item'),
    path('remove-item-complete',complete_remove,name='complete_remove'),
    path('',show_cart,name='get_cart'),
    path('discount_code',discount_code,name='discount_code')
]