from django.urls import path
from .views import CartAPIView, cartDelete

urlpatterns = [
    path('cart/', CartAPIView.as_view()),
    path('cart/delete/', cartDelete.as_view()),
]