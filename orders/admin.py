from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display_links = ('id', 'product')
    list_display = ('id', 'product', 'get_shop', 'full_name', 'address',
                    'phone_number', 'email', 'completed', 'date_ordered')
    list_filter = ('date_ordered', 'completed','product__shop')
    search_fields = ('full_name', 'address', 'product__name')
    list_per_page = 50
    
    def get_shop(self, obj):
        return obj.product.shop
    get_shop.short_description = 'Dokan'


admin.site.register(Order, OrderAdmin)
