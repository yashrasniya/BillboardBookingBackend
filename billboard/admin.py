from django.contrib import admin
from .models import BillBoard,Address,Images,BannerType,LocationType,bookingHistory
from reviews.models import Review
# Register your models here.
class Images_admin(admin.TabularInline):
    model = Images
class Review_admin(admin.TabularInline):
    model = Review


@admin.register(BillBoard)
class ModelNameAdmin(admin.ModelAdmin):
    inlines = [Images_admin,Review_admin]

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
@admin.register(BannerType)
class BannerTypeAdmin(admin.ModelAdmin):
    pass
@admin.register(LocationType)
class LocationTypeAdmin(admin.ModelAdmin):
    pass
@admin.register(bookingHistory)
class BookingHistoryAdmin(admin.ModelAdmin):
    pass
