from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from operator import attrgetter


def welcomepage(request):
    if request.user.is_authenticated:
        return render(request, "auctions/in.html")
    else:
        return render(request, "auctions/login.html")


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

def cat_display(request, title):
    category = Category.objects.get(name=title)
    listings = Listing.objects.filter(item_category=category)
    return render(request, "auctions/cat_disp.html", {
        "category":category,
        "listings":listings
    })

def add(request):
    if request.method == "POST":
        title2 = request.POST["title"]
        description2 = request.POST["description"]
        price2 = request.POST["price"]
        owner2 = request.user
        category_id2 = request.POST["category"]
        category2 = Category.objects.get(id=category_id2)
        photo2 = request.POST["photo"]
        listings = Listing.objects.all()
        titles = []
        for listing in listings:
            titles.append(listing.title)
        if title2 not in titles:
            new = Listing(title=title2, description=description2, price=price2, photo=photo2, owner=owner2, item_category=category2)
            new.save()
            return display(request, title2)
        else:
            return render(request, "auctions/add.html", {
                "message":"This title already exists, please try another one.",
                "categories": Category.objects.all()
            } )
    else:
        return render(request, "auctions/add.html", {
            "categories": Category.objects.all()
        })

def display(request, name):
    you = request.user
    listing2 = Listing.objects.get(title = name)
    bid_problem = False
    if request.method=="POST":
        datetime2 = datetime.now()
        if 'comm' in request.POST:
            new_comm = request.POST["comm"]
            comment2 = Comment(comment=new_comm, listing=listing2, datetime=datetime2, writer=you)
            comment2.save()
        elif 'bid' in request.POST:
            new_bid = int(request.POST["bid"])
            if new_bid >listing2.price:
                listing2.price = new_bid
                bid2 = Bid(value=new_bid, item=listing2, datetime=datetime2, user=you)
                bid2.save()
            else:
                bid_problem = True
                bid_message="Your bid wasn't placed, new bids need to be higher than the best"
    bids = listing2.its_bids.all().order_by('-datetime') 
    comments = listing2.its_comments.all().order_by('-datetime')
    adding = False
    moving = False
    if you.is_authenticated:
        moving = True
        if listing2 in you.watchlist.all():
            adding = False
        else :
            adding = True 
    else:
        moving = False
    if bid_problem:
        return render(request, "auctions/display.html", {
            "listing": listing2,
            "moving": moving,
            "adding":adding,
            "comments":comments,
            "bids": bids,
            "bid_message": bid_message
        })
    else:
        return render(request, "auctions/display.html", {
            "listing": listing2,
            "moving": moving,
            "adding":adding,
            "comments":comments,
            "bids": bids,
        })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })    


@login_required
def watchlist(request):
    you =  request.user
    favlist = you.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "favlist": favlist
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

@login_required
def watch(request, name):
    you = request.user
    item = Listing.objects.get(title=name)
    you.watchlist.add(item)
    return watchlist(request)

@login_required
def unwatch(request, name):
    you = request.user
    item = Listing.objects.get(title=name)
    you.watchlist.remove(item)
    return watchlist(request)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


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
