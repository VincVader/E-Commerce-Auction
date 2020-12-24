from django import forms
from .models import Listing, Bid, Comment

class NewBid(forms.ModelForm):
    class Meta:
        model = Bid
        fields = {"bid_value"}
        labels = {
            "bid_value": "Place your bid"
        }

class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {"message"}


class NewListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = {"title", "description", "start_bid", "image", "category"}
    
