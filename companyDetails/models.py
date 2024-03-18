from django.db import models


# Create your models here.
class company_Details(models.Model):
    name = models.CharField(max_length=40)
    mobile_number = models.CharField(max_length=40)
    emailID = models.CharField(max_length=40)
    logo = models.ImageField(upload_to='company_details/logo')
    address = models.TextField(max_length=400)
    mapUrl = models.URLField(max_length=1000)


class OurCompany(models.Model):
    name = models.CharField(max_length=40)
    logo = models.ImageField(upload_to='OurCompany/logo')


class OurServicesDetails(models.Model):
    name = models.CharField(max_length=40)
    image = models.ImageField(upload_to='OurServicesDetails/img')
    details = models.TextField(max_length=2000)
