from django.shortcuts import render
from openai import OpenAI
from .serializers import generationsHistorySerializer
from .models import generationsHistory,openAiConfig
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import pagination,status

from rest_framework.permissions import IsAuthenticated
import os

try:
    obj=openAiConfig.objects.first()
    if obj.server_on:

        client = OpenAI(api_key=obj.api_key)
        print(client.api_key,obj.api_key)


except Exception as e:
    print(e)
    obj=False
    client = False

class GenerationsHistory(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = generationsHistorySerializer
    pagination_class =pagination.PageNumberPagination

    def get_queryset(self):
        return generationsHistory.objects.filter(user=self.request.user)


class ImageGenerations(APIView):
    permission_classes = [IsAuthenticated]
    def error_message(self,message,status=400):
        return Response({'error':message},status=status)

    def post(self, request, format=None):
        if request.data.get('text',''):
            text = request.data.get('text')
            print(client)
            if obj and obj.server_on and client:
                re = client.images.generate(
                  model=obj.model_name,
                  prompt=text,
                  n=1,
                  size=obj.img_size
                )
                dir(re)
                if re.data:
                    gen_obj=generationsHistory.objects.create(text=text,user=self.request.user,img_url=re.data[0].url)
                    return Response(generationsHistorySerializer(gen_obj).data,status=200)
                else:
                    return self.error_message('model error',status.HTTP_400_BAD_REQUEST)
            else:
                return self.error_message('server Ai model is not working',status.HTTP_400_BAD_REQUEST)
        return self.error_message('test is missing',status.HTTP_400_BAD_REQUEST)



