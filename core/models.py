from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



# Create your models here.
class registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    User_Name = models.CharField(max_length=50, null=False)
    Email = models.EmailField(unique=True, null=False)
    Password = models.CharField(max_length=100)
    def __str__(self):
        return self.User_Name
    
class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
