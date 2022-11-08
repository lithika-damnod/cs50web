from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Post(models.Model): 
    post_id = models.AutoField(primary_key=True)
    content = models.TextField(blank=False)
    creator = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
    n_likes = models.IntegerField(default=0) 
    posted_time = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField('User', related_name='liked_users', blank=True)

    def __str__(self): 
        return f"""
            post_id: {self.post_id},
            creator_id: {self.creator.id}, 
            likes: {self.n_likes}, 
            posted_time: {self.posted_time}, 
            content: {self.content}
            likers: {self.likers}
    """