from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from shop.models import Category, Product, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'prod', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'email', 'body')


admin.site.register(Comment, CommentAdmin)


class ProductAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'

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
    form = ProductAdminForm
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


# @admin.register(Reviews)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'parent', 'product', 'id')
#     readonly_fields = ('name', 'email')