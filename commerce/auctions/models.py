from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORIES = (
        
        ('SDN', 'SEDAN'),
        ('COP', 'COUPE'),
        ('SPC', 'SPORTS CAR'),
        ('STW', 'STATION WAGON'),
        ('HTB', 'HATCHBACK'),
        ('CVT', 'CONVERTIBLE'),
        ('SUV', 'SPORT-UTILITY VEHICLE'),
        ('MNV', 'MINIVAN'),
        ('PUT', 'PICKUP TRUCK'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default= 1, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    start_bid = models.IntegerField()
    image = models.ImageField(upload_to='img',default='default.jpg', blank=True)
    category = models.CharField(max_length=3, choices=CATEGORIES, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)
    active = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return f"ID: {self.pk} {self.title} {self.start_bid}$"

class Auction(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    number_of_bids = models.IntegerField()
    current_bid = models.IntegerField(blank=True)
    current_leader = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    def __str__(self):
	    return f"ID: {self.pk} Listing: {self.listing_id.pk} Bids: {self.number_of_bids} Current Bid {self.current_bid}"

class Bid(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    listing_id = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True, null=True)
    bid_value = models.IntegerField(blank=True)

    def __str__(self):
        return f" User: {self.user_id} Listing id: {self.listing_id.pk} Bid: {self.bid_value}."
 
class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    message_time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f" User: {self.user_id} On {self.listing_id.pk} Said: {self.message} at {self.message_time}."

class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f" User: {self.user_id}. Listing in watchlist: {self.listing_id.pk}."

