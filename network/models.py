from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("User", related_name="following")

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    likes = models.ManyToManyField("User", related_name="liked", null=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def likes_count(self):
        return self.likes.count() if self.likes else 0

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "title": self.title,
            "body": self.body,
            "created": self.created.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes.count() if self.likes != None else 0,
        }