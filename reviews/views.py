from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import review_serializer
# Create your views here.
class review_create(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        ser_obj=review_serializer(data=request.data)
        if ser_obj.is_valid():
            ser_obj.save(user=request.user)
        else:
            return Response(ser_obj.errors)
        return Response(ser_obj.data)
