from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import AppUser, Post

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = AppUser

admin.site.register(AppUser, CustomUserAdmin)

class PostAdmin(admin.ModelAdmin):
    model = Post
    readonly_fields = ('id', 'slug')

admin.site.register(Post, PostAdmin)
