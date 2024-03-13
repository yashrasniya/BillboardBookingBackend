from rest_framework import serializers
from ..models import Address,BillBoard,Images,bookingHistory
from reviews.serializers import review_serializer,Review
from BillboardBooking.utilitys import image_add_db


class Images_serializer(serializers.ModelSerializer):
  class Meta:
    model = Images
    fields = [
      'img'
    ]
class cities(serializers.ModelSerializer):
  class Meta:
    model=Address
    fields=[
      'city'
    ]

class Address_serializers(serializers.ModelSerializer):
  class Meta:
    model=Address
    fields='__all__'



class BillBoard_serializers(serializers.ModelSerializer):
  images=serializers.SerializerMethodField()
  reviews=serializers.SerializerMethodField()
  rating=serializers.SerializerMethodField()
  location_type=serializers.SerializerMethodField()
  banner_type=serializers.SerializerMethodField()
  address=Address_serializers()
  class Meta:
    model=BillBoard
    fields=[
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

    ]
  def get_images(self,obj):
    return Images_serializer(Images.objects.filter(billboard=obj),many=True,context=self.context).data
  def get_reviews(self,obj):
    return review_serializer(Review.objects.filter(billboard=obj),many=True).data
  def get_rating(self,obj):
    rating=0
    count=0
    for i in Review.objects.filter(billboard=obj):
      rating=i.rating
      count+=1

    return rating/count

  def get_address(self,obj):
    return str(obj.address)
  def get_location_type(self,obj):
    return str(obj.location_type)
  def get_banner_type(self,obj):
    return str(obj.banner_type)

class BookingHistorySerializer(serializers.ModelSerializer):
  billboard=serializers.SerializerMethodField()
  user=serializers.SerializerMethodField()
  payment=serializers.SerializerMethodField()
  class Meta:
    model=bookingHistory
    fields='__all__'

  def get_user(self,obj):
    return obj.user.name()

  def get_billboard(self, obj):
    return BillBoard_serializers(obj.billboard,context=self.context).data

  def get_payment(self,obj):
    return obj.payment.short_url