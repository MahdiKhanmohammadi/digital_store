from django.urls import path
from .views import get_author_comment, product_category,articel_category,product_detail,add_comment,blog_detail

urlpatterns = [
    path("category/<str:slug>",product_category,name='category_products'),
    path("category/articel/<str:slug>",articel_category,name='category_articel'),
    path('product/<slug>',product_detail,name='product_detail'),
    path('blog/<pk>',blog_detail,name='blog_detail'),
    path("comment/add",add_comment,name='add_comment'),
    path('get_author_comment',get_author_comment),
]