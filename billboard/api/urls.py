from django.urls import path
from .views import cities_list, address_list, billBoard, BillBoardHistoryViewSet, BillBoardHistoryCartViewSet

urlpatterns = [
    path('citiesList/', cities_list.as_view()),
    path('addressList/', address_list.as_view()),
    path('billBoard/', billBoard.as_view()),
    path('billBoard/<int:id>', billBoard.as_view()),
    path('billBoard/history/', BillBoardHistoryViewSet.as_view()),
    path('billBoard/history/cart/', BillBoardHistoryCartViewSet.as_view()),
]