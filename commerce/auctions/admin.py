from django.contrib import admin

from .models import Listing, User, Bid, Comment, Watchlist, Auction

# Register your models here.

admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Auction)
