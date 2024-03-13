from django.urls import path
from .views import GenerationsHistory,ImageGenerations
urlpatterns = [
    path('generations/history/',GenerationsHistory.as_view() ),
    path('image/generations/',ImageGenerations.as_view() ),

]