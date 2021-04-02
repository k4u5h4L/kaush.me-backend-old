from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from users.models import CustomUser

# Create your models here.

class Tag(models.Model):
    tag_name = models.CharField(max_length=25)

    def __str__(self):
        return self.tag_name


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile_pic.png', upload_to='blog_covers')
    post_title = models.CharField(max_length=200)
    post_text = models.TextField(max_length=5000)
    post_timestamp = models.DateTimeField(default=timezone.now)

    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.post_title


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=500)
    comment_timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment_text

class Contact(models.Model):
    contact_name = models.CharField(max_length=200)
    contact_email = models.CharField(max_length=100)
    contact_message = models.TextField(max_length=5000)

    def __str__(self):
        return self.contact_name