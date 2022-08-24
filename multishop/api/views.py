from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from shop.models import Product, Comment, Category

from .serializers import ProductSerializer, ProductDetailSerializer, CommentSerializer, CategorySerializer


@api_view(['GET'])
def prods(request):
    if request.method == 'GET':
        prods = Product.objects.filter(available=True)
        serializer = ProductSerializer(prods, many=True)
        return Response(serializer.data)


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductDetailSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments(request, pk):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = Comment.objects.filter(active=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def cats(request):
    if request.method == 'GET':
        cats = Category.objects.all()
        serializer = CategorySerializer(cats, many=True)
        return Response(serializer.data)