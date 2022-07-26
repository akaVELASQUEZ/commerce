from random import choices
from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from .choices import CATEGORY_CHOICES

class User(AbstractUser):
    pass

class Listings(models.Model):
    name = models.CharField(max_length=200)
    img = models.CharField(max_length=200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    description = models.CharField(max_length=500)
    min_bid = models.FloatField()
    current_bid = models.FloatField()
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)
    highest_bidder = models.CharField(max_length=200, null=True, blank=True)

class Bids(models.Model):
    list_id = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="list_bids")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders_id")
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders_name")
    bid = models.FloatField()

class Comments(models.Model):
    list_id = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="list_comments")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenters_id")
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenters_name")
    date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=500)

class Watchlist(models.Model):
    list_id = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="list_watchlist")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist_id")
    status = models.BooleanField(default=False)
