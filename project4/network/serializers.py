from rest_framework import serializers
from django.db import models
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class PostSerializer(serializers.ModelSerializer):
    posted_time = serializers.DateTimeField(format="%b %d %Y, %I:%M %p")
    creator = serializers.StringRelatedField(read_only=True)

    class Meta: 
        model = Post
        fields = "__all__"
        read_only_fields = ['posted_time', 'creator']
