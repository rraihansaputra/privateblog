from functools import partial

from django.shortcuts import render

from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from allauth.socialaccount.models import SocialApp

import twitter

from core.models import Post, AppUser
from core.forms import PostForm


def Home(request):
    return render(request, "home.html")

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = AppUser
    slug_field = "username"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self,form):
        form.instance.author = self.request.user
        form.instance.status = 1
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self,form):
        form.instance.status = 1
        return super().form_valid(form)

# Create your views here.
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):

        # verify that user viewing is following the author on twitter
        # TODO can use UserPassesTestMixin and use handle_no_permission to redirect
        # https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin
        user = request.user
        author = AppUser.objects.get(username=kwargs["author"])

        # TODO possibility of hitting the database repeatedly
        # can use .select_related
        user_socialaccount = user.socialaccount_set.get()
        user_tokens = user_socialaccount.socialtoken_set.get()
        user_id = user_socialaccount.uid
        author_id = author.socialaccount_set.get().uid

        # don't trigger API if author is the viewer
        if user_id == author_id:
            return super().get(self.request, *args, **kwargs)

        # Prepare the Twitter API to fetch the data
        twitter_app = SocialApp.objects.get(provider="twitter")

        t_api = twitter.Api(
            consumer_key = twitter_app.client_id,
            consumer_secret = twitter_app.secret,
            access_token_key = user_tokens.token,
            access_token_secret = user_tokens.token_secret,
        )

        # TODO cache the friends list and refresh every minute instead of
        # looking up friendship every single time
        try:
            user_is_following_author = t_api.LookupFriendship(author_id)[0].connections['following']
        except twitter.TwitterError as err:
            print(err.message)
            if err.message[0]["code"] == 88: # too many requests error
                return render(request, 'core/twitter_rate_limit.html', status=429)

        if user_is_following_author == False:
            return render(request, 'core/no_follow.html',
                context={"author": author},
                status=401)

        return super().get(self.request, *args, **kwargs)
