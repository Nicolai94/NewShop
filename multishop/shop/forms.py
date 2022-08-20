from django import forms
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'email': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        captcha = CaptchaField()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField()


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Subject', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField()


# class UserReviewForm(forms.ModelForm):
#     class Meta:
#         model = Reviews
#         exclude = {'is_active'}
#         widgets = {'product': forms.HiddenInput}


# class GuestReviewForm(forms.ModelForm):
#     captcha = CaptchaField(label='Input text photo', error_messages={'invalid': 'Incorrect text'})
#
#     class Meta:
#         model = Reviews
#         exclude = {'is_active'}
#         widgets = {'product': forms.HiddenInput}


# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Reviews
#         fields = ('name', 'email', 'message')
