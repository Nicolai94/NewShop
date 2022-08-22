from django.urls import path

from .views import *

app_name = 'orders'
urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('created/', checkout, name='checkout'),
    path('admin/order/<order_id>/', admin_order_detail, name='admin_order_detail'),
]