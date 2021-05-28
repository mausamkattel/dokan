from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'owner', 'category',
                    'block', 'hide', 'is_trusted', 'featured', 'limited', 'date_added')
    list_editable = ('block', 'hide', 'is_trusted', 'featured', 'limited')
    list_per_page = 50
    list_filter = ('date_added', 'block', 'hide',
                   'is_trusted', 'featured', 'limited')
    search_fields = ('name', 'address', 'description')
    list_display_links = ('id', 'name')


@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'block')
    list_display_links = ('id', 'title')
    list_editable = ('block',)
