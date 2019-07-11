from functools import partial

from django.shortcuts import render

from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from allauth.socialaccount.models import SocialApp

import twitter

from core.models import Post, AppUser

twitter_app = SocialApp.objects.get(provider="twitter")

t = partial(twitter.Api,
    consumer_key = twitter_app.client_id,
    consumer_secret = twitter_app.secret,
)

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

        user_tokens = user.socialaccount_set.get().socialtoken_set.get()
        author_id = author.socialaccount_set.get().uid

        t_api = t(
            access_token_key = user_tokens.token,
            access_token_secret = user_tokens.token_secret
        )

        # TODO cache the friends list and refresh every minute instead of
        # looking up friendship every single time
        try:
            user_is_following_author = t_api.LookupFriendship(author_id)[0].connections['following']
        except twitter.TwitterError as err:
            print(err.message)
            if err.message[0]["code"] == 88: #
                return render(request, 'core/twitter_rate_limit.html', status=429)

        if user_is_following_author == False:
            return render(request, 'core/no_follow.html',
                context={"author": author},
                status=401)

        return super().get(self.request, *args, **kwargs)
