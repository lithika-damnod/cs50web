from django.utils import timezone
from typing_extensions import Self
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return f"{self.category}"
class Listing(models.Model):
    title = models.CharField(max_length=60)
    created_date = models.DateTimeField(default=timezone.now)
    description = models.CharField(null=True, max_length=300)
    startingBid = models.FloatField()
    currentBid = models.FloatField()
    pic_url = models.CharField(null=False, max_length=300) #picture url
    category = models.ManyToManyField(Category, blank=True, related_name="product_cat")
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="creator")
    watchers = models.ManyToManyField(User, blank=True, related_name="watched_ppl")
    buyer = models.ManyToManyField(User, blank=True, related_name="buyers")
    watchList = models.ManyToManyField(User, blank=True, related_name="watchlist")
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"title: {self.title} Starting Bid: {self.startingBid}"

class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"auction: {self.auction} user: {self.user} \n description: {self.comment}" 