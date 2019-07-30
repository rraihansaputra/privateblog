from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.utils.text import slugify

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from django.utils.http import int_to_base36
from uuid import uuid4 as uuid

# Create your models here.
class AppUser(AbstractUser):
    # custom user model to accomodate future changes
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.username

def pkgen():
    # generate random base36 string for Post primary key
    # https://stackoverflow.com/questions/3759006/#comment92949575_3812628
    return int_to_base36(uuid().int)[:8]

class Post(models.Model):
    STATUS = (
        (0, "Draft"),
        (1, "Publish"),
    )

    id = models.CharField(max_length=8, primary_key=True, default=pkgen)
    author = models.ForeignKey(AppUser, on_delete = models.CASCADE, related_name = "blog_posts")
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=100,
        editable=False,
        )
    body = RichTextUploadingField(config_name='default')
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    last_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug,
            'author': self.author.username,
        }
        return reverse("post-detail", kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['-created_on']
        unique_together = ('author', 'id')

    def __str__(self):
        return self.title
