from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from shop.views import Home, ProductByCategory, GetProduct, contact, Search, ShopList, about, login, register


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', ProductByCategory.as_view(), name='category'),
    path('product/<str:slug>/', GetProduct.as_view(), name='detail'),
    path('contact/', contact, name='contact'),
    path('search/', Search.as_view(), name='search'),
    path('shop/', ShopList.as_view(), name='shop_list'),
    path('about/', about, name='about'),
    path('sign_in/', login, name='login'),
    path('sign_up/', register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)