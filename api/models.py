import requests
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """Custom User model that extends AbstractUser and adds an email field and a verification status."""

    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_tokens(self):
        from rest_framework_simplejwt.tokens import RefreshToken

        fun_date = requests.get("https://worldtimeapi.org/api/timezone/Africa/Lome")
        refresh = RefreshToken.for_user(self)
        refresh["username"] = self.username
        refresh["email"] = self.email
        refresh["first_name"] = self.first_name
        refresh["last_name"] = self.last_name
        refresh["fun_date"] = fun_date.json()["datetime"]
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class Blog(models.Model):
    """Model representing a blog post."""

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    """Meta information about the blog post."""

    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    """Model representing a comment on a blog post.²"""

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.blog.title}"

    """Meta information about the comment."""

    class Meta:
        ordering = ["-created_at"]
