from django.urls import path

from .views import prods, ProductDetailView, comments, cats

urlpatterns = [
    path('prods/', prods),
    path('prods/<int:pk>/', ProductDetailView.as_view()),
    path('prods/<int:pk>/comments', comments),
    path('cats/', cats)
    ]