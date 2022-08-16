from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Category
from cart.forms import CartAddProductForm

from .forms import UserLoginForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'shop/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your registration success')
            return redirect('home')
    else:
        form = UserCreationForm()
        messages.error(request, 'Wrong registration')
    return render(request, 'shop/register.html', {'form': form})


class Home(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Product.objects.filter(available=True).order_by('-created')[:8]


class ProductByCategory(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'products'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class GetProduct(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'


def contact(request):
    return render(request, 'shop/contact.html')


class Search(ListView):
    template_name = 'shop/search.html'
    context_object_name = 'search'

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


class ShopList(ListView):
    model = Product
    template_name = 'shop/shop_list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Товары'
        return context

    def get_queryset(self):
        return Product.objects.filter(available=True)


def about(request):
    return render(request, 'shop/about.html')


def product_detail(request, id_prod):
    product = get_object_or_404(Product, id=id_prod,   available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/detail.html',
                  {'product': product, 'cart_product_form': cart_product_form})


