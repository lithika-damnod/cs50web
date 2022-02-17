from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("wiki/<str:filename>", views.loadPage, name="loadpage"), 
    path("create/", views.createEntry, name="createentry")
]
