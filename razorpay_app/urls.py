from django.urls import path,include
from .views import *


urlpatterns = [
    path('create_payment_link/<bill_board_id>', create_payment_link.as_view()),
    path('payment_verify/', verify_payment.as_view()),
    path('transaction_history/', TransactionHistory.as_view()),

]
