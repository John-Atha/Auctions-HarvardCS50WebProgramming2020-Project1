from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', related_name = "fans")

class Category(models.Model):
    name = models.CharField(max_length=64, null=True)
    photo = models.ImageField(default="", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    photo = models.ImageField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sells")
    item_category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE, related_name="its_category")
    active = models.BooleanField(default="True")
    best_bidder = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="gets")

    def __str__(self):
        return f"{self.title}, {self.item_category}, {self.active}, {self.photo}"


class Comment(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="its_comments")
    datetime = models.DateTimeField(default=datetime.now)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="made_comments")

    def __str__(self):
        return f"{self.listing}, {self.datetime}, {self.writer}"    

class Bid(models.Model):
    value = models.PositiveIntegerField()
    datetime = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biddings")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="its_bids") 

    def __str__(self):
        return f"{self.user}, {self.value}, {self.datetime}, {self.item}" 

 