from rest_framework import serializers
from django.db import models
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'n_followers', 'followers']

class PostSerializer(serializers.ModelSerializer):
    posted_time = serializers.DateTimeField(format="%b %d %Y, %I:%M %p")
    creator = UserSerializer()
    class Meta: 
        model = Post
        exclude = ['likers']
        read_only_fields = ['posted_time', 'creator']
