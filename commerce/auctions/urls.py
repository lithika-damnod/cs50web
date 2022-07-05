from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("listings/<str:id>", views.display_listings, name="displayListings"), 
    path("create", views.createListing, name="create"),
    path("watchlist", views.showWatchList, name="watchlist"), 
    path("categories", views.showCats, name="showCategories"), 
    path("categories/<str:id>", views.listDownCats, name="listCats"),  
    path("api/add/comment", views.addComment, name="addComment"), 
    path("api/add/watchlist", views.addWatchList, name="addWatchList"), 
    path("api/remove/watchlist", views.removeWatchList, name="removeWatchList"), 
    path("api/add/bid", views.addBid, name="newBid"), 
    path("api/close/bid", views.closeBidding, name="closeBidding")
]
