from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import User, Category, Listing, Bit, Comment


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allcategories = Category.objects.all()
    return render(request, "auctions/index.html",{
                "listings": activeListings,
                "categories": allcategories,
    })

def listing(request, id):
    listingData = Listing.objects.get(pk=id) 
    allbits = Bit.objects.filter(listing=listingData)
    allcomments = Comment.objects.filter(listing = listingData)
    isOwner = request.user.username == listingData.owner.username
    if request.user.is_authenticated:
        isListingInWatchList = request.user in listingData.watchlist.all()
    else:
        isListingInWatchList = False
    return render(request, "auctions/listing.html", {
            "listing": listingData,
            "isListingInWatchList": isListingInWatchList,
            "allbits": allbits,
            "allcomments": allcomments,
            "isOwner": isOwner
    })


def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    if request.user.is_authenticated:
        isListingInWatchList = request.user in listingData.watchlist.all()
    else:
        isListingInWatchList = False
    
    allcomments = Comment.objects.filter(listing = listingData)
    isOwner = request.user.username == listingData.owner.username

    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchList": isListingInWatchList,
        "allcomments": allcomments,
        "isOwner": isOwner,
        "update" : True,
        "message": "congratulations! Your Auction is closed",
    })


@require_POST
def removeWatchList(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

@require_POST
def addWatchList(request, id):
    print(f"Adding listing {id} to user {request.user}")
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def displayWatchList(request):
    currentUser = request.user
    listings = currentUser.listingWatchList.all()
    return render(request, "auctions/watchList.html",{
        "listings": listings
    })


def addbit(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    isOwner = request.user.username == listingData.owner.username



    try:
        newbit_value = float(request.POST['newbit'])
    except (ValueError, KeyError):
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "isListingInWatchList": currentUser in listingData.watchlist.all(),
            "allbits": Bit.objects.filter(listing=listingData),
            "allcomments": Comment.objects.filter(listing=listingData),
            "message": "Invalid bid amount.",
            "update": False,
            "isOwner": isOwner,

        })

    if newbit_value > listingData.price.bit:
        newbit = Bit.objects.create(
            author=currentUser,
            listing=listingData,
            bit=newbit_value
        )
        listingData.price = newbit
        listingData.save()

        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "isListingInWatchList": currentUser in listingData.watchlist.all(),
            "allbits": Bit.objects.filter(listing=listingData),
            "allcomments": Comment.objects.filter(listing=listingData),
            "message": "Bid placed successfully!",
            "update": True,
            "isOwner": isOwner,

        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "isListingInWatchList": currentUser in listingData.watchlist.all(),
            "allbits": Bit.objects.filter(listing=listingData),
            "allcomments": Comment.objects.filter(listing=listingData),
            "message": "Your bid must be higher than the current price.",
            "update": False,
            "isOwner": isOwner,
        })



def addcomment(request, id):
    currentUser = request.user
    listinData = Listing.objects.get(pk=id)
    comments = request.POST['newcomment']

    newcomment = Comment(
        author = currentUser,
        listing = listinData,
        comment = comments,
    )

    newcomment.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))


def displayCategory(request):
    if request.method == "POST":
        category_name = request.POST['category']
        cat = Category.objects.get(categoryName=category_name)
        activeListings = Listing.objects.filter(isActive=True, Category=cat)
        allcategories = Category.objects.all()
        return render(request, "auctions/index.html",{
                    "listings": activeListings,
                    "categories": allcategories,
        })

def create_Listing(request):
    if request.method == "GET":
        allcategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allcategories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]

        currentUser = request.user

        # Get the category instance
        categoryData = Category.objects.get(categoryName=category)

                # First, create the Listing without the price
        newListing = Listing(
            title=title,
            description=description,
            imageurl=imageurl,
            Category=categoryData,
            owner=currentUser
        )
        newListing.save()

        # Now create the Bit and assign the new listing
        bit_val = Bit(
            bit=float(price),
            author=currentUser,
            listing=newListing
        )
        bit_val.save()

        # Assign the bit as the starting price (if price is a ForeignKey)
        newListing.price = bit_val
        newListing.save()

        return HttpResponseRedirect(reverse(index))


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
