from django.contrib import admin
from .models import Product, Customer, OrderPlaced, Cart
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
# def customer_info(self,obj):
#     link = reverse('admin:core_customer_change', args=[obj.Customer.pk])
#     return format_html('<a href="{}">{}</a>',link,obj.Customer.name)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'brand', 'category']

# @admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'ordered_date', 'status']


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']



admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(OrderPlaced,OrderPlacedAdmin)

