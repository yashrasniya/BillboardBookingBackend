from django.urls import path
from .views import review_create
urlpatterns = [
    path('reviews/create/', review_create.as_view()),

]