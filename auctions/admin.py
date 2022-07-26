from xml.etree.ElementTree import Comment
from django.contrib import admin

from .models import Bids, Comments, Listings, User, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Watchlist)
admin.site.register(Comments)