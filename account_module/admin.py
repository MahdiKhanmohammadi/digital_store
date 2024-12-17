from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    fields = ('email','is_active','first_name','last_name')
    list_display =  [ 'email' , 'is_active' , 'first_name' , 'last_name']








admin.site.register(User , UserAdmin)