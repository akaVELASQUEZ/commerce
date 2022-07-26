from operator import truediv
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .choices import CATEGORY_CHOICES
from .models import Bids, Comments, Listings, User, Watchlist

class CategoryForm(forms.Form):
    category = forms.ChoiceField(choices = CATEGORY_CHOICES, label="", initial='', widget=forms.Select(), required=True)


def index(request):
    return render (request, "auctions/index.html", {
        "listings": Listings.objects.filter(status = True).order_by("-date")
    })

def create(request):
    if request.method == "POST":
        _name = request.POST["_name"]
        _img = request.POST["_img"]
        _description = request.POST["_description"]
        _min = request.POST["_min"]
        _category = request.POST["_category"]
        listing = Listings.objects.create(
            name=_name, img=_img, user_id=request.user, description=_description, min_bid=_min, current_bid=_min, category=_category)
        return HttpResponseRedirect(reverse("index"))
    else:
        x = len(CATEGORY_CHOICES)
        val = []
        ph = []
        for i in range(x):
            val.append(CATEGORY_CHOICES[i][0])
            ph.append(CATEGORY_CHOICES[i][1])
        
        fusion = zip(val, ph)
        return render(request, "auctions/create.html", {
            "fusion": fusion
        })

def listing(request, list_id):
    if request.method == "POST":
        status = request.POST["status"]
        listing = Listings.objects.get(id = list_id)
        if status == "Close Listing":
            listing.status = False
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=(list_id,)))

    else:
        listing = Listings.objects.get(id = list_id)

        listing_bids = Bids.objects.filter(list_id = list_id).order_by("-bid")
        if not listing_bids:
            listing_bids = None
        
        listing_comments = Comments.objects.filter(list_id = list_id).order_by("-date")
        if not listing_comments:
            listing_comments = None

        listing_watchlist = Watchlist.objects.filter(list_id=list_id).filter(user_id=request.user.id)
        if listing_watchlist:
            watchlist_status = listing_watchlist[0].status
        else:
            watchlist_status = False

        if request.user.is_authenticated:
            sign_in = True
        else:
            sign_in = False

        user_id = request.user

        if listing.user_id.id == user_id.id:
            sign_op = True
        else:
            sign_op = False

        return render(request, "auctions/listing.html", {
            "listing": listing, "listing_bids": listing_bids, "listing_comments": listing_comments,
            "sign_in": sign_in, "sign_op": sign_op, "watchlist_status": watchlist_status
        })


def bid(request, list_id):
    if request.method == "POST":
        bid = float(request.POST["bid"])
        listing = Listings.objects.get(id = list_id)
        if bid > listing.current_bid:
            listing.current_bid = bid
            listing.highest_bidder = request.user.username
            listing.save()
            highest_bid = Bids.objects.create(
                list_id = listing, user_id = request.user, user_name = request.user, bid=bid
            )
            return HttpResponseRedirect(reverse("listing", args=(list_id,)))
        else:
            return render(request, "auctions/error.html", {
                "listing": listing
            })


def watchlist(request, list_id):
    if request.method == "POST":
        watchlist_status = request.POST["watchlist"]
        if watchlist_status == "True":
            watchlist_status = True
        else:
            watchlist_status = False
        listing = Listings.objects.get(id = list_id)
        watchlist = Watchlist.objects.filter(list_id=list_id).filter(user_id=request.user.id)
        if watchlist:
            watchlist[0].status = watchlist_status
            watchlist[0].save()
            return HttpResponseRedirect(reverse("listing", args=(list_id,)))
        else:
            new = Watchlist.objects.create(
                list_id = listing, user_id = request.user, status = watchlist_status
            )
            return HttpResponseRedirect(reverse("listing", args=(list_id,)))

def comment(request, list_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        listing = Listings.objects.get(id = list_id)
        if comment:
            new_comment = Comments.objects.create(
                list_id = listing, user_id = request.user, user_name = request.user, comment=comment
            )
            return HttpResponseRedirect(reverse("listing", args=(list_id,)))

def user_watchlist(request):
    user_wl = Watchlist.objects.filter(user_id = request.user.id).filter(status = True)
    wl_id = []
    for wl in user_wl:
        wl_id.append(wl.list_id.id)
    user_watchlist = Listings.objects.filter(id__in=wl_id)
    return render (request, "auctions/watchlist.html", {
        "user_watchlist": user_watchlist
    })

def category(request, category):
    category_search = CATEGORY_CHOICES[int(category)][1]
    list = Listings.objects.filter(category=category).filter(status = True)
    return render (request, "auctions/category.html", {
        "list": list, "category_search": category_search
    })

def user_listing(request):
    user_active = Listings.objects.filter(user_id = request.user.id).filter(status = True).order_by("-date")
    user_closed = Listings.objects.filter(user_id = request.user.id).filter(status = False).order_by("-date")
    return render (request, "auctions/user_listing.html", {
        "user_active": user_active, "user_closed": user_closed
    })

def closed(request):
    return render (request, "auctions/closed.html", {
        "listings": Listings.objects.filter(status = False).order_by("-date")
    })

def search(request):
    result = []
    search = request.GET.get("q")
    lists = Listings.objects.all()
    for list in lists:
        if search.lower().strip() in list.name.lower():
            result.append(list)

    return render(request, "auctions/search.html", {
            "result": result
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
