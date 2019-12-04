from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import AppUser, Post

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = AppUser
        fields = ('username', 'full_name')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = AppUser
        fields = ('username', 'full_name')

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'body',
        ]
