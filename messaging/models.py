from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class CustomUser(User):
    class Meta:
        proxy = True

    # Add your custom methods or properties here
    def full_name(self):
        return f"{self.first_name} {self.last_name}"




class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    interests = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} at {self.created_at}"
