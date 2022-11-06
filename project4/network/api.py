from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import *
from .serializers import * 

""" Post Manipulating API endpoints """

@api_view(['POST'])
def create_post(request): 
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)
    elif request.method == "POST": 
        json_str = json.dumps(request.data)
        post_content = json.loads(json_str)["content"]
        user_obj = User.objects.get(username=request.user)
        new_post = Post(content=post_content, creator=user_obj)
        new_post.save()
        return JsonResponse({
            "status": "success"
        }, status=201)
    return JsonResponse({ 
        "error": "method not allowed"
    })

@api_view(['GET', 'PUT', 'DELETE'])
def single_post(request, post_id): 
    if request.method == "GET":
        try: 
            all_posts = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return Response({
                "error": "Post not found"
            }, status=404)
        serialized = PostSerializer(all_posts)
        return Response(serialized.data)
    elif request.method == "PUT": 
        if not request.user.is_authenticated: 
            return JsonResponse({
                "error": "unauthorized"
            }, status=401)

        # check for permisions 
        post_obj = Post.objects.get(post_id=post_id)
        owner_user_obj = User.objects.get(username=post_obj.creator)
        req_user_obj = User.objects.get(username=request.user)
        if owner_user_obj.id != req_user_obj.id :
            return JsonResponse({
                "error": "unauthorized"
            }, status=401)

        json_str = json.dumps(request.data)
        json_data = json.loads(json_str)
        post_obj.content = json_data["content"]
        post_obj.save()
        return JsonResponse({
            "status": "success"
        })
    elif request.method == "DELETE":
        if not request.user.is_authenticated: 
            return JsonResponse({
                "error": "unauthorized"
            }, status=401)

        # check for permisions and proceed 
        post_obj = Post.objects.get(post_id=post_id)
        owner_user_obj = User.objects.get(username=post_obj.creator)
        req_user_obj = User.objects.get(username=request.user)
        if owner_user_obj.id != req_user_obj.id :
            return JsonResponse({
                "error": "unauthorized"
            }, status=401)

        post_obj.delete()
        return JsonResponse({
            "status": "success"
        })

@api_view(['GET'])
def all_posts(request): 
    all_posts = Post.objects.all().order_by("-posted_time")
    serialized = PostSerializer(all_posts, many=True)
    return Response(serialized.data)

@api_view(['GET'])
def single_user(request, user_id): 
    user_obj = User.objects.get(id=user_id)
    user_serialized = UserSerializer(user_obj)
    user_posts = Post.objects.filter(creator=user_obj).order_by("-posted_time")
    user_posts_serialized = PostSerializer(user_posts, many=True)
    json_res = { 
        "creator":user_serialized.data, 
        "posts": user_posts_serialized.data 
    }
    return Response(json_res)