from rest_framework import serializers
from BillboardBooking.utilitys import image_add_db
from .models import Review


class review_serializer(serializers.ModelSerializer):
  user=serializers.SerializerMethodField()
  class Meta:
    model=Review
    fields=[
      'billboard',
      'user',
      'text',
      'datetime',
      'rating',
    ]
    extra_kwargs = {
      'billboard': {'required': True},
      'text': {'required': True},
      'rating': {'required': True},
    }

  def get_user(self,obj):
      return obj.user.name()