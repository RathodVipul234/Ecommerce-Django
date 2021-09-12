from django import template
from django.apps import apps
from core.models import Cart

register = template.Library()


@register.filter
def count_amount(value):
    products = value
    amount = 0
    for i in products:
        amount = amount + (i.product.discounted_price * i.quantity)
    return amount


@register.filter
def total_amount(value):
    amount = count_amount(value)
    shipping = 40
    amount = amount + shipping
    return amount

@register.simple_tag()
def product_price(qty, unit_price, *args, **kwargs):
    return qty * unit_price

