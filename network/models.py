from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey("User", on_delete=models.PROTECT)
    body = models.TextField(blank=True)
    likes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "title": self.title,
            "body": self.body,
            "created": self.created.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes,
            "comments": None
        }

class Comment(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)