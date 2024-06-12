from django.contrib import admin
from .models import CartItem
# Register your models here.
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass

