from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Category
from cart.forms import CartAddProductForm
from .forms import UserLoginForm, ContactForm, CommentForm


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'shop/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


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


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    comments = product.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.prod = product
            new_comment.name = comment_form.cleaned_data['name']
            new_comment.email = comment_form.cleaned_data['email']
            new_comment.body = comment_form.cleaned_data['body']
            new_comment.save()
            messages.add_message(request, messages.SUCCESS, 'Review added')
    else:
        comment_form = CommentForm()
        messages.add_message(request, messages.WARNING, 'Review not added')
    return render(request, 'shop/detail.html',
                  {'product': product, 'cart_product_form': cart_product_form, 'comment_form': comment_form, 'comments': comments})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], ' ',
                             [' '], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'shop/contact.html', context)


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

