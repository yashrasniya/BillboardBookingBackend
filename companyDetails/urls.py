from django.urls import path
from .views import companyDetailsViews,OurCompanyDetailsViews,OurServicesDetailsViews
urlpatterns = [
    path('company/details/', companyDetailsViews.as_view()),
    path('our/company/', OurCompanyDetailsViews.as_view()),
    path('our/services/', OurServicesDetailsViews.as_view()),

]