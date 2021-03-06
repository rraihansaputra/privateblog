"""privateblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from core.views import Home, PostDetailView, PostCreateView, PostUpdateView, ProfileDetailView

urlpatterns = [
    path('', Home),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path(r'ckeditor/', include('ckeditor_uploader.urls')),
    path('post/', PostCreateView.as_view(), name='post-create'),
    path('<str:slug>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('<str:author>/<str:slug>-<str:pk>/edit', PostUpdateView.as_view(), name='post-detail'),
    path('<str:author>/<str:slug>-<str:pk>/', PostDetailView.as_view(), name='post-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
