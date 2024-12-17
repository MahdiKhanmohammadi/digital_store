from django.contrib import admin
from django.core.exceptions import ValidationError
import jdatetime
from .models import Ad
# Register your models here.

class AdAdmin(admin.ModelAdmin):
    list_display = ['title','url','expire_date','visibel']
    list_editable =['visibel']
    

admin.site.register(Ad,AdAdmin)