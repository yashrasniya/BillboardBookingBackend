from rest_framework import serializers

from billboard.api.serializers import BillBoard_serializers
from cart.models import CartItem


class cart_serializer(serializers.ModelSerializer):
  billboard=BillBoard_serializers()
  class Meta:
    model = CartItem
    fields = '__all__'