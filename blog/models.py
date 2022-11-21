from django.db import models
# from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=50)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일
    tag = models.ManyToManyField(Tag, related_name='posts')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True) # 작성자


class PostLike(models.Model):
    user = models.ForeignKey(User, related_name = 'likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일