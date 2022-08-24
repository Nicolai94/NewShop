from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.signing import BadSignature
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Category, AdvUser
from cart.forms import CartAddProductForm
from .forms import ContactForm, CommentForm, ChangeUserInfoForm, RegisterUserForm
from .utilities import signer


@login_required
def profile(request):
    return render(request, 'shop/profile.html')


class ShopLoginView(LoginView):
    template_name = 'shop/login.html'


class ShopLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'shop/logout.html'


class ShopPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'shop/password_change.html'
    success_url = reverse_lazy('shop:profile')
    success_message = 'Password is changed'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'shop/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('shop:profile')
    success_message = 'Data of user changed'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'shop/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'shop/user_is_activated.html'
    else:
        template = 'shop/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'shop/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'shop/register_done.html'

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'shop/delete_user.html'
    success_url = reverse_lazy('index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'User delete')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


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

