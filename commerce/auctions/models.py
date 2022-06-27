from django.utils import timezone
from typing_extensions import Self
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.category}"
class Listing(models.Model):
    title = models.CharField(max_length=60)
    created_date = models.DateTimeField(default=timezone.now)
    description = models.CharField(null=True, max_length=300)
    startingBid = models.FloatField()
    currentBid = models.FloatField()
    pic_url = models.CharField(null=False, max_length=300) #picture url
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_cat")
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="creator")
    watchers = models.ManyToManyField(User, blank=True, related_name="watched_ppl")
    buyer = models.ForeignKey(User, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f"title: {self.title} Starting Bid: {self.startingBid}"

class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.FloatField()
    date = models.DateTimeField(default=timezone.now)