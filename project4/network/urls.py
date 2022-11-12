from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 

    # REST api endpoints
    path("api/post", views.create_post, name="posts"), 
    path("api/post/<int:post_id>", views.single_post, name="single_post"),
    path("api/post/<int:post_id>/liked", views.like_status, name="like_status"),
    path("api/posts", views.all_posts, name="all_posts"),
    path("api/user/<int:user_id>/", views.single_user, name="single_user"),
]
