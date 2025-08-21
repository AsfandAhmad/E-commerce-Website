from django.contrib import admin
from .models import User, Category, Listing, Bit, Comment
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bit)
admin.site.register(Comment)
