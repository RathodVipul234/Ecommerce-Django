from django.contrib import admin
from .models import Product, Customer, OrderPlaced, Cart
from django.utils.html import format_html
from django.urls import reverse


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'brand', 'category']

class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'ordered_date', 'status']


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']



admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(OrderPlaced,OrderPlacedAdmin)

