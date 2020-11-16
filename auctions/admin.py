from django.contrib import admin

# Register your models here.
from .models import *

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "item_category", "price", "owner", "best_bidder", "active")

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "products")

    def products(self, obj: Category):
        counter = Listing.objects.filter(item_category=obj.id).count()
        return f"{counter}"

    products.short_description='Products#'

class CommentAdmin(admin.ModelAdmin):
    list_display = ("writer", "item", "datetime")

    def item(self, obj: Comment):
        return f"{obj.listing.title}"
    
    item.short_description='Listing'

class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "value", "datetime")

    def listing(self, obj: Bid):
        return f"{obj.item.title}"


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)