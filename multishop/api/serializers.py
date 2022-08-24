from rest_framework import serializers

from shop.models import Product, Comment, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'content', 'price', 'stock', 'created', 'category')


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'slug', 'content', 'price', 'stock', 'created', 'category', 'photo', 'available')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('prod', 'name', 'email', 'body', 'created', 'active')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', 'photo')