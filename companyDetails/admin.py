from django.contrib import admin
from .models import company_Details,OurServicesDetails,OurCompany
# Register your models here.

admin.site.register(company_Details)
admin.site.register(OurServicesDetails)
admin.site.register(OurCompany)