from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import company_Details, OurCompany, OurServicesDetails
from .serializers import OurCompanySerializer, OurServicesDetailsSerializer, company_DetailsSerializer


# Create your views here.
class companyDetailsViews(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = company_DetailsSerializer
    queryset = company_Details.objects.all()


class OurServicesDetailsViews(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = OurServicesDetailsSerializer
    queryset = OurServicesDetails.objects.all()


class OurCompanyDetailsViews(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = OurCompanySerializer
    queryset = OurCompany.objects.all()
