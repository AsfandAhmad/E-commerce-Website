from django.contrib.auth.models import AbstractUser
from django.db import models 


class User(AbstractUser):
    pass
    

class Category(models.Model):
    categoryName = models.CharField(max_length=50)


    def __str__(self):
        return self.categoryName


class Bit(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userbit")
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="bids")
    bit = models.FloatField(max_length= 500)

    def __str__(self):
        return f"${self.bit:.2f} by {self.author}"
    
class Listing(models.Model):
    title = models.CharField(max_length=30) 
    imageurl = models.CharField(max_length=1000)
    price = models.ForeignKey("Bit", on_delete=models.CASCADE, blank=True, null=True, related_name="bidprice")
    description = models.CharField(max_length= 500)
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, related_name="listingWatchList")
    

    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    comment = models.CharField(max_length= 200)

    def __str__(self):
        return f"{self.author} comment's on {self.listing}"