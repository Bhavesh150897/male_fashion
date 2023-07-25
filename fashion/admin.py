from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class SliderAdmin(admin.ModelAdmin):
    model = Slider
    list_display = ['name', 'description', ]

class SizeAdmin(admin.ModelAdmin):
    model = Size
    list_display = ['name', ]

class ColorAdmin(admin.ModelAdmin):
    model = Color
    list_display = ['name', ]

class VariationAdmin(admin.ModelAdmin):
    model = Variation
    list_display = ['product', 'size', 'color', ]

class ProductAdmin(SummernoteModelAdmin,admin.ModelAdmin):
    model = Product
    summernote_fields = 'long_desc'
    list_display = ['category','brand', 'name','label', 'product_image', 'quantity', 'original_price','discounted_price', 'desc', 'status', 'trending', ]

class CatagoryAdmin(admin.ModelAdmin):
    model = Catagory
    list_display = ['name','description','status','created_at', ]

class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ['name','slug','created_at', ]

class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ['user','first_name','last_name','country','address','city','zipcode','state','email','phone','created_at', ]

class OrderPlacedAdmin(admin.ModelAdmin):
    model = OrderPlaced
    list_display = ['user','customer','product','quantity','ordered_date','status','amount','order_id','razorpay_payment_id','has_paid','created_at', ]
    
admin.site.register(Slider,SliderAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Catagory,CatagoryAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(OrderPlaced,OrderPlacedAdmin)