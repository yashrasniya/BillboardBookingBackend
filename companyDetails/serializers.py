from rest_framework import serializers
from .models import company_Details,OurCompany,OurServicesDetails
from reviews.serializers import review_serializer,Review

class company_DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = company_Details
        fields = '__all__'

class OurCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = OurCompany
        fields = '__all__'

class OurServicesDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurServicesDetails
        fields = '__all__'
