from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from .models import CartItem
from cart.seriailzers import cart_serializer
from billboard.models import BillBoard


class CartAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class =cart_serializer
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def delete(self,request,*args,**kwargs):
        print(self.request.data.get('cart_id',''))
        if not self.request.data.get('cart_id',''):
            return Response({'status': '404', 'message': 'Not found', 'error':"cart_id id not found body"},
                                status=status.HTTP_404_NOT_FOUND)
        if not CartItem.objects.filter(id=self.request.data.get('cart_id')):
            return Response({'status': '404', 'message': 'Not found', 'error':"cart_id id not found"},
                                status=status.HTTP_404_NOT_FOUND)
        cart = CartItem.objects.get(id=self.request.data.get('cart_id'))
        cart.delete()
        return Response({'status': '200', 'message': 'done'},
                                status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        if not self.request.data.get('billboard_id'):
            return Response({'status': '404', 'message': 'Not found', 'error': "billboard_id id not found body"},
                            status=status.HTTP_404_NOT_FOUND)
        if not BillBoard.objects.filter(id=self.request.data.get('billboard_id')):
            return Response({'status': '404', 'message': 'Not found', 'error': "cart_id id not found"},
                            status=status.HTTP_404_NOT_FOUND)
        if CartItem.objects.filter(user=self.request.user,billboard=BillBoard.objects.get(id=self.request.data.get('billboard_id'))):
            return Response({'status': '200', 'message': 'already added'},status=200)
        cart = CartItem.objects.create(user=self.request.user,billboard=BillBoard.objects.get(id=self.request.data.get('billboard_id')))

        return Response(cart_serializer(cart,context={'request': request}).data,
                        status=status.HTTP_200_OK)

class cartDelete(APIView):
    permission_classes = [IsAuthenticated]



    def post(self,request):

        print(self.request.data.get('cart_id', ''))
        if not self.request.data.get('cart_id', ''):
            return Response({'status': '404', 'message': 'Not found', 'error': "cart_id id not found body"},
                            status=status.HTTP_404_NOT_FOUND)
        if not CartItem.objects.filter(id=self.request.data.get('cart_id')):
            return Response({'status': '404', 'message': 'Not found', 'error': "cart_id id not found"},
                            status=status.HTTP_404_NOT_FOUND)
        cart = CartItem.objects.get(id=self.request.data.get('cart_id'))
        cart.delete()
        return Response({'status': '200', 'message': 'done'},
                        status=status.HTTP_200_OK)

