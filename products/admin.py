from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'shop', 'price',
                    'in_stock', 'featured', 'block')
    list_display_links = ('id', 'name')
    list_filter = ('date_added', 'block', 'featured', 'in_stock')
    search_fields = ('name', 'shop__name', 'description', 'sub_title')
    list_per_page = 100
    list_editable = ('block', 'featured')
