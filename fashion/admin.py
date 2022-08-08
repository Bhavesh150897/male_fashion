from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class SliderAdmin(admin.ModelAdmin):
    model = Slider
    list_display = ['name', 'description', ]

class ProductAdmin(SummernoteModelAdmin,admin.ModelAdmin):
    model = Product
    summernote_fields = 'long_desc'
    list_display = ['category','brand', 'name','label', 'product_image', 'quantity', 'original_price','discounted_price', 'desc', 'status', 'trending', ]

class CatagoryAdmin(admin.ModelAdmin):
    model = Catagory
    list_display = ['name','description','status','created_at', ]

class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ['name','created_at', ]

admin.site.register(Slider,SliderAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Catagory,CatagoryAdmin)
admin.site.register(Brand,BrandAdmin)
