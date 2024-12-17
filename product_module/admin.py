from django.contrib import admin
from jalali_date import datetime2jalali,date2jalali
from account_module.models import User
from .models import Category, Discount, Product, ProductAttribute,Blog,Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields ={"slug": ["title"]}


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['discount_percent','discount_expire']
    list_filter = ['discount_percent','discount_expire']


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'format_price', 'description']
    prepopulated_fields ={"slug": ["title"]}
    inlines = [ProductAttributeInline]
    

    readonly_fields = ['get_discount_price']


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['product', 'key', 'value']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','short_description','jalali_created_at']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == 'author':
            kwargs['queryset'] = User.objects.filter(is_staff = True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

class CommentAdmin(admin.ModelAdmin):
    list_display=['body','read_by_admin',"visibel",'created_at']
    list_editable = ['read_by_admin','visibel']
    exclude = ['created_at']
    list_filter = ['read_by_admin','visibel']
    ordering = ['created_at']

#region register
admin.site.register(Category, CategoryAdmin)
admin.site.register(Discount,DiscountAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Comment,CommentAdmin)
#endregion