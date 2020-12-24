from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import NewBid, NewListing, NewComment
from .models import User, Listing, Bid, Comment, Auction, Watchlist, Comment
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.contrib import messages



def index(request):
    listings = Listing.objects.filter(active=True)

    for item in listings:
        auction = Auction.objects.get(listing_id=item.id)
        item.category = item.get_category_display()
        item.start_bid=auction.current_bid
        if request.user.is_authenticated:
            try:
                watchlist = Watchlist.objects.get(user_id=request.user, listing_id=auction)
                item.in_watch_list = True
            except Watchlist.DoesNotExist:
                item.in_watch_list = False

        else:
            in_watch_list = ''
            

    if request.user.is_authenticated:
        watchlist_items = len(Watchlist.objects.filter(user_id=request.user))        
    else:
        watchlist_items = 0
    
    return render(request, "auctions/index.html",{
        "bruh": listings,        
        "watchlist_items": watchlist_items,
        
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

def watchlistbtn(request):
    if request.method == 'POST':
        watchlist_user = request.user
        watchlist_listing = request.POST["watchlist_listing"]
        peep = Auction.objects.get(listing_id=watchlist_listing)
        try:
            watchlist = Watchlist.objects.get(listing_id=peep, user_id=watchlist_user)
            watchlist.delete()

        except Watchlist.DoesNotExist:
            w0 = Watchlist(listing_id=peep, user_id=watchlist_user)
            w0.save()
            

        return HttpResponseRedirect(reverse("listings", kwargs={'list_id':watchlist_listing}))
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required
def newbid(request, list_id):
    auction = Auction.objects.get(listing_id=list_id)
    form = NewBid(request.POST)
    if form.is_valid():
        raisebid = form.save(commit=False)
        raisebid.user_id = request.user
        raisebid.listing_id = auction
        
        if raisebid.bid_value <= auction.current_bid:
            messages.error(request, 'Your bid is too small. It must be bigger than:')
            return HttpResponseRedirect(reverse("listings", kwargs={'list_id':list_id}))
        else:
            raisebid.save()
            auction.number_of_bids+=1
            auction.current_bid=raisebid.bid_value
            auction.current_leader=request.user
            auction.save()
            messages.success(request, 'Successfully raised bid:')
            return HttpResponseRedirect(reverse("listings", kwargs={'list_id':list_id}))
            
    else:
        pass

@login_required
def watchlist_items(request):
    watchlist = Watchlist.objects.filter(user_id=request.user)
    qs = []
    for item in watchlist:
        listings = Listing.objects.get(id=item.listing_id.pk)
        qs += [listings]
    
    watchlist_items = len(watchlist)        
    
    
    return render(request, "auctions/watchlist.html",{
        "bruh": qs,        
        "watchlist_items": watchlist_items,
        
    })


def listings(request, list_id):
    listing = Listing.objects.get(id=list_id)
    listing.category = listing.get_category_display()
    addcomment = NewComment()
    form = NewBid()
    in_watch_list = False
    comments = Comment.objects.filter(listing_id=list_id)
    try:
        auction = Auction.objects.get(listing_id=list_id)
        number_of_bids = auction.number_of_bids
    except Auction.DoesNotExist:
        auction.number_of_bids = 0
        auction.current_bid = listing.start_bid

    if request.user.is_authenticated:
        watchlist_items = len(Watchlist.objects.filter(user_id=request.user))

        try:
            watchlist = Watchlist.objects.get(user_id=request.user, listing_id=auction)
            in_watch_list = True
        except Watchlist.DoesNotExist:
            in_watch_list = False

    else:
        watchlist_items = 0 

    return render(request, "auctions/listing.html",{
        "item": listing,
        "addcomment": addcomment,
        "comments": comments,
        "form": form,
        "auction": auction,
        "watchlist_items": watchlist_items,
        "in_watch_list": in_watch_list,
    })
    

@login_required
def create_listing(request): 
    form = NewListing()      
    watchlist_items = len(Watchlist.objects.filter(user_id=request.user))  
    
    if request.method == "POST":
        form = NewListing(request.POST or None, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            peep = get_object_or_404(Listing, id=listing.id)            
            form = NewBid()
            bid0 = Auction(listing_id=peep, number_of_bids=0, current_bid=listing.start_bid, current_leader=request.user)
            bid0.save()
            return HttpResponseRedirect(reverse("listings", kwargs={'list_id':peep.id}))  
        else:
            return render(request, "auctions/new-listing.html", {
            "form": form,
            "watchlist_items": watchlist_items,
        })
        
    else:
        return render(request, "auctions/new-listing.html", {
            "form": form,
            "watchlist_items": watchlist_items,
        })

@login_required
def categories(request):
    category = Listing.objects.first()
    watchlist_items = len(Watchlist.objects.filter(user_id=request.user)) 
    categories = category.CATEGORIES
    
    return render(request, "auctions/categories.html", {
            "watchlist_items": watchlist_items,
            "categories": categories,
        })

@login_required
def category(request, cat):
    
    listings = Listing.objects.filter(category=cat)
    for item in listings:
        auction = Auction.objects.get(listing_id=item.id)
        item.category = item.get_category_display()
        item.start_bid=auction.current_bid
        try:
            watchlist = Watchlist.objects.get(user_id=request.user, listing_id=auction)
            item.in_watch_list = True
        except Watchlist.DoesNotExist:
            item.in_watch_list = False

    watchlist_items = len(Watchlist.objects.filter(user_id=request.user))        
    
    
    return render(request, "auctions/category.html",{
        "bruh": listings,        
        "watchlist_items": watchlist_items,
        
        
    })

@login_required
def close_auction(request, list_id):
    listing = Listing.objects.get(id=list_id)
    listing.active = False
    auction = Auction.objects.get(listing_id=list_id)
    listing.save()
    try:
        bid = Bid.objects.get(listing_id=list_id, bid_value=auction.current_bid)
    except Bid.DoesNotExist:
        bid=0

    messages.warning(request, 'Successfully closed auction.')
    
    


    return HttpResponseRedirect(reverse("listings", kwargs={'list_id':list_id})) 

@login_required
def comment(request, list_id):
    form = NewComment(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user_id = request.user
        comment.listing_id = Auction.objects.get(listing_id=list_id)
        comment.save()
        return HttpResponseRedirect(reverse("listings", kwargs={'list_id':list_id})) 

    else:
        return HttpResponseRedirect(reverse("listings", kwargs={'list_id':list_id})) 
