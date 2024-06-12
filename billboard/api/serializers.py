from rest_framework import serializers
from ..models import Address, BillBoard, Images, bookingHistory
from reviews.serializers import review_serializer, Review
from BillboardBooking.utilitys import image_add_db
import random
import datetime
from cart.models import CartItem
from  django.contrib.auth.models import AnonymousUser
from drf_extra_fields.fields import Base64ImageField
class Images_serializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'img'
        ]


class cities(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'city'
        ]


class Address_serializers(serializers.ModelSerializer):
    full_address = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = '__all__'

    def get_full_address(self, obj):
        return ' '.join([obj.address, obj.landmark, obj.city, obj.state, obj.country])


class BillBoard_serializers(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    location_type = serializers.SerializerMethodField()
    banner_type = serializers.SerializerMethodField()
    is_added_in_cart = serializers.SerializerMethodField()
    last_booking_date = serializers.SerializerMethodField()
    address = Address_serializers()

    class Meta:
        model = BillBoard
        fields = [
            'id',
            'address',
            'price',
            'size',
            'location_type',
            'banner_type',
            'description',
            'images',
            'reviews',
            'rating',
            'is_added_in_cart',
            'last_booking_date',

        ]

    def get_images(self, obj):
        return Images_serializer(Images.objects.filter(billboard=obj), many=True, context=self.context).data

    def get_reviews(self, obj):
        return review_serializer(Review.objects.filter(billboard=obj), many=True).data

    def get_rating(self, obj):
        rating = 0
        count = 0
        for i in Review.objects.filter(billboard=obj):
            rating = i.rating
            count += 1
        if count > 0:
            return rating / count
        return random.randint(3, 5)

    def get_address(self, obj):
        return str(obj.address)

    def get_location_type(self, obj):
        return str(obj.location_type)

    def get_banner_type(self, obj):
        return str(obj.banner_type)

    def get_is_added_in_cart(self, obj):
        if self.context.get('request') and type(self.context.get('request').user)!=AnonymousUser:
            if CartItem.objects.filter(user=self.context['request'].user,billboard=obj):
                return True
        return False

    def get_last_booking_date(self,obj):
        billboard_obj=bookingHistory.objects.filter(billboard=obj,end_date__gt=datetime.datetime.today())
        print(billboard_obj)
        if billboard_obj:
            date=billboard_obj[0].end_date
            for i in billboard_obj[1:]:
                print(i.end_date,date)
                if date<i.end_date:
                    date=i.end_date
            return date
        return None


class BookingHistorySerializer(serializers.ModelSerializer):
    billboard = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()
    image = Base64ImageField()


    class Meta:
        model = bookingHistory
        fields = '__all__'

    def get_user(self, obj):
        return obj.user.name()

    def get_billboard(self, obj):
        return BillBoard_serializers(obj.billboard, context=self.context).data

    def get_payment(self, obj):
        return obj.payment.short_url
