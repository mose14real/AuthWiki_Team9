import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models


def auth_lib_image_file_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join('uploads', 'authlib', filename)


# Create your models here.
class CodeSnippet(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    auth_library = models.ForeignKey('AuthLibrary',
                                     on_delete=models.CASCADE,
                                     related_name='code_snippet')

    def __str__(self):
        return f"{self.title} || {str(self.id)}"


class AuthLibrary(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    no_of_downloads = models.PositiveIntegerField()
    created_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, upload_to=auth_lib_image_file_path)

    def __str__(self):
        return f"{self.name}"


class Reaction(models.Model):
    upvote = models.IntegerField(default=0)
    down_vote = models.IntegerField(default=0)

    def __str__(self):
        return f"{str(self.upvote)}"


class Comment(models.Model):
    author_name = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True)
    comment_body = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    auth_library = models.ForeignKey(AuthLibrary, on_delete=models.CASCADE,
                                     related_name='comment')

    # reaction = models.OneToOneField(Reaction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.author_name)}"


class Category(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='Description')

    def __str__(self):
        return str(self.name)
