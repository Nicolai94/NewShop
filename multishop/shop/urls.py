from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import Home, ProductByCategory, contact, Search, ShopList, about, ShopLogoutView, \
    product_detail, ShopLoginView, profile, ChangeUserInfoView, ShopPasswordChangeView, RegisterUserView, \
    RegisterDoneView, user_activate, DeleteUserView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', ProductByCategory.as_view(), name='category'),
    path('product/<str:slug>/', product_detail, name='product_detail'),
    path('contact/', contact, name='contact'),
    path('search/', Search.as_view(), name='search'),
    path('shop/', ShopList.as_view(), name='shop_list'),
    path('about/', about, name='about'),
    path('account/sign_in/', ShopLoginView.as_view(), name='login'),
    # path('account/sign_up/', register, name='register'),
    path('account/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('account/logout/', ShopLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', ShopPasswordChangeView.as_view(), name='password_change'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)