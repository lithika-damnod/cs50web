from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category


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
        return render(request, "auctions/listings.html", {
            "list_id": id
        })

def createListing(request): 
    if request.method == "POST": 
        title = request.POST["title"]
        description = request.POST["description"]
        init_bid = request.POST["init-bid"]
        pic_url = request.POST["pic-url"]
        print(f"{title} \n {description} \n initial bid: {init_bid} url: {pic_url}")
        cat = Category.objects.first() 
        curr_usr = User.objects.get(username="lithika")
        newEntry = Listing(title=title, description=description, startingBid=init_bid, currentBid=init_bid, pic_url=pic_url, category=cat, creator=curr_usr) 
        newEntry.save()
        return HttpResponseRedirect(reverse("index"))
    else: 
        return render(request, "auctions/create.html")