from django.contrib import admin
from .models import Category, Product

admin.site.register(Category)
admin.site.register(Product)

from .models import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)