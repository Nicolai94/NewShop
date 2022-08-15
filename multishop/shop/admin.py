from django.contrib import admin
from django.utils.safestring import mark_safe

from shop.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_photo']
    prepopulated_fields = {'slug': ('name',)}

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url }" width="50">')
        return '-'

    get_photo.short_description = 'Миниатюра'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'stock', 'available', 'created', 'get_photo')
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url }" width="50">')
        return '-'

    get_photo.short_description = 'Миниатюра'