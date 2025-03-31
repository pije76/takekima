from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from .models import *

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'description', 'unit', 'stock', 'balance', 'created_at')
    ModelAdmin.ordering = ('id',)

    class Meta:
        model = Item

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'date', 'description', 'item_code', 'quantity', 'unit_price', 'header_code')
    ModelAdmin.ordering = ('id',)

    class Meta:
        model = Purchase

class SellAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'date', 'description', 'item_code', 'quantity', 'header_code')
    ModelAdmin.ordering = ('id',)

    class Meta:
        model = Sell


admin.site.register(Item, ItemAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Sell, SellAdmin)
