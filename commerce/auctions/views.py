from tkinter import W
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Bid, Comment


def index(request):
    allListings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "entries" : allListings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def display_listings(request, id):
    if request.method == "POST":
        pass
    else:
        # get data for the corresponding id
        data = Listing.objects.get(id=id)
        # get the usernamem of the bid conductor 
        username = User.objects.get(username=data.creator) 
        # add watcher :TODO (NOT TESTED) 
        try:
            viewer = User.objects.get(id=request.user.id)
        except User.DoesNotExist:  
            # add new watcher 
            update_object = Listing.objects.get(id=id)
            update_object.watchers.add(viewer)
            update_object.save()

        # get the auction object
        auction_object = Listing.objects.get(id=id)
        # search for comments for the viewing listing
        all_comments = Comment.objects.filter(auction=auction_object)

        return render(request, "auctions/listings.html", {
            "list_id": id, 
            "data": data, 
            "username": username, 
            "comments": all_comments
        })

def createListing(request): 
    if request.method == "POST": 
        # POST Data
        title = request.POST["title"]
        description = request.POST["description"]
        init_bid = request.POST["init-bid"]
        pic_url = request.POST["pic-url"]
        print(f"{title} \n {description} \n initial bid: {init_bid} url: {pic_url}")
        # get selected categories as a list 
        cats = request.POST.getlist("cat"); 
        for i in cats: 
            #search each category to find whether it's present in the category tab already, and it it doesn't add it or just use it if it's there
            try: 
                record = Category.objects.get(category=i)    
            except Category.DoesNotExist: 
                newCat = Category(category=i)
                newCat.save() 

        # get the id of current signed in user
        curr_usr = User.objects.get(id=request.user.id)
        print(f"user: {curr_usr}")
        # Add new entry to Listing table
        newEntry = Listing(title=title, description=description, startingBid=init_bid, currentBid=init_bid, pic_url=pic_url, creator=curr_usr) 
        # Start the Bid with the intial bid of the creator 
        newEntry.save()
        # add Each category to newEntry
        for c in cats: 
            newEntry.category.add(c) 

        newEntry.save() 

        newBid = Bid(auction=newEntry, user=curr_usr, offer=init_bid) 
        newBid.save()
        
        return HttpResponseRedirect(reverse("index"))
    else: 
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "cats" : categories
        })

def showWatchList(request):
    return render(request, "auctions/watchlist.html")

# API Calls 
def addComment(request): 
    if request.method == "POST":
        comment_desc = request.POST["comment-text"]   
        list_id = request.POST["list_id"]
        # add comment to the db 
        auc = Listing.objects.get(id=list_id)
        curr_user = User.objects.get(id=request.user.id)
        newComment = Comment(auction=auc, user=curr_user, comment=comment_desc)
        newComment.save()
        print(f"new comment: {comment_desc} id: {list_id}")
        return HttpResponseRedirect("/listings/" + list_id)
    else:
        return JsonResponse({
            "error":"method not allowed", 
            "allowed":["POST"]
        })

def showCats(request):
    all_categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories" : all_categories
    })

def listDownCats(request, id):
    cat_object = Category.objects.get(category=id)
    results = Listing.objects.filter(category=cat_object)
    return render(request, "auctions/listCats.html", {
        "id" : id, 
        "results": results  
    })