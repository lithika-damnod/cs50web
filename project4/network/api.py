from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import *
from .serializers import * 

PAGES_PER_PAGE = 10
""" Post Manipulating API endpoints """

@api_view(['GET'])
def current_user(request): 
    if not request.user.is_authenticated:
        return Response({
            "error": "user must be logged in" 
        })
    curr_user_obj = User.objects.get(username=request.user)
    serializer = UserSerializer(curr_user_obj)
    return Response(serializer.data)

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

@api_view(['GET', 'PUT'])
def like_status(request, post_id): 
    if not request.user.is_authenticated: 
        return JsonResponse({
            "error": "unauthorized"
        }, status=401)

    if request.method == "GET": 
        try: 
            post_obj = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return Response({
                "status": "error", 
                "error": "post not found"
            }, status=404)

        try: 
            likers = post_obj.likers.get(username=request.user)
        except User.DoesNotExist:
            return Response({
                "status": False 
            })
        return Response({
            "status": True
        })
    else: 
        try: 
            post_obj = Post.objects.get(post_id=post_id) 
        except Post.DoesNotExist:
            return Response({"error": "post not found"}, status=404)

        # trigger true and false.. initially true
        try: 
            liker = post_obj.likers.get(username=request.user) 
        except User.DoesNotExist:
            post_obj.likers.add(request.user)

            # increment like count 
            curr_likes = post_obj.n_likes 
            post_obj.n_likes = curr_likes + 1

            post_obj.save()
            return Response({
                "status": True
            }) 

        # if the liker is already in it 
        post_obj.likers.remove(request.user)
        # decrement like count 
        curr_likes = post_obj.n_likes 
        # possible error
        if curr_likes-1 < 0:
            post_obj.n_likes = 0
        else: 
            post_obj.n_likes = curr_likes - 1

        post_obj.save()

        return Response({
            "status": False
        })


@api_view(['GET'])
def all_posts(request): 
    all_posts = Post.objects.all().order_by("-posted_time")
    postPaginator = Paginator(all_posts, PAGES_PER_PAGE) 
    page = request.GET.get('page')
    filtered_posts = postPaginator.get_page(page)
    serialized = PostSerializer(filtered_posts, many=True)
    return_serialized_data = {
        "posts":serialized.data,
        "paginator": {
            "total_pages": postPaginator.num_pages,
            "current_page": filtered_posts.number,
            "has_next": filtered_posts.has_next(),
            "has_prev": filtered_posts.has_previous(),
        }
    }
    return Response(return_serialized_data)

@api_view(['GET'])
def single_user(request, user_id): 
    user_obj = User.objects.get(id=user_id)
    user_serialized = UserSerializer(user_obj)
    user_posts = Post.objects.filter(creator=user_obj).order_by("-posted_time")
    postPaginator = Paginator(user_posts, PAGES_PER_PAGE) 
    page = request.GET.get('page')
    filtered_posts = postPaginator.get_page(page)
    user_posts_serialized = PostSerializer(filtered_posts, many=True)
    json_res = { 
        "creator":user_serialized.data, 
        "posts": user_posts_serialized.data, 
        "paginator": {
            "total_pages": postPaginator.num_pages,
            "current_page": filtered_posts.number,
            "has_next": filtered_posts.has_next(),
            "has_prev": filtered_posts.has_previous(),
        }
    }
    return Response(json_res)


@api_view(['GET', 'PUT'])
def follow_events(request, user_id):
    if not request.user.is_authenticated: 
        return JsonResponse({
            "error": "unauthorized"
        }, status=401)
    elif request.method == 'GET': 
        try: 
            user_object = User.objects.get(id=user_id)
        except User.DoesNotExist: 
            return Response({
                "error": "user not found"
            })
        try: 
            user_followers = user_object.followers.get(username=request.user)
        except User.DoesNotExist:
            return Response({
                "status": False
            })
        return Response({
            "status": True
        })
    elif request.method == 'PUT': 
        try: 
            user_obj = User.objects.get(id=user_id) 
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=404)

        # trigger true and false.. initially true
        try: 
            follower = user_obj.followers.get(username=request.user) 
        except User.DoesNotExist:
            user_obj.followers.add(request.user)

            # increment like count 
            curr_followers = user_obj.n_followers
            user_obj.n_followers = curr_followers + 1

            user_obj.save()
            return Response({
                "status": True
            }) 
        # if the liker is already in it 
        user_obj.followers.remove(request.user)
        # decrement like count 
        curr_followers = user_obj.n_followers
        # possible error
        if curr_followers-1 < 0:
            user_obj.n_followers = 0
        else: 
            user_obj.n_followers = curr_followers - 1

        user_obj.save()

        return Response({
            "status": False
        })
    return Response({
        "error": "method not allowed"
    })

@api_view(['GET'])
def following_posts(request): 
    if not request.user.is_authenticated: 
        return Response({})
    following = User.objects.filter(followers=request.user)
    following_posts = Post.objects.filter(creator__in=following).order_by("-posted_time")
    postPaginator = Paginator(following_posts, PAGES_PER_PAGE) 
    page = request.GET.get('page')
    filtered_posts = postPaginator.get_page(page)
    serialized = PostSerializer(filtered_posts, many=True) 
    return_embedded_data = { 
        "posts": serialized.data,
        "paginator": {
            "total_pages": postPaginator.num_pages,
            "current_page": filtered_posts.number,
            "has_next": filtered_posts.has_next(),
            "has_prev": filtered_posts.has_previous(),
        }
    }
    return Response(return_embedded_data)