from django.shortcuts import render

from django.views.generic import DetailView

from core.models import Post

# Create your views here.
class PostDetailView(DetailView):
    model = Post
    query_pk_and_slug = True
