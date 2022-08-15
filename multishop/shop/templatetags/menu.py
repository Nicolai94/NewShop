from django import template
from shop.models import Category


register = template.Library()

@register.inclusion_tag('shop/category_tpl.html')
def show_menu(menu_class='menu'):
    categories = Category.objects.all()
    return {'categories': categories, 'menu_class': menu_class}


@register.inclusion_tag('shop/category_main_tpl.html')
def show_menu1(menu_main='menu'):
    categories = Category.objects.all()
    return {'categories': categories, 'menu_class': menu_main}