from rest_framework import serializers
from .models import generationsHistory



class generationsHistorySerializer(serializers.ModelSerializer):
  class Meta:
    model = generationsHistory
    fields = '__all__'







