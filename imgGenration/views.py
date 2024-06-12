from django.shortcuts import render
from openai import OpenAI
from .serializers import generationsHistorySerializer
from .models import generationsHistory,openAiConfig
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import pagination,status
from gradio_client import Client
from django.core.files import File  # you need this somewhere
client = Client("yashrasniya/stabilityai-stable-diffusion-xl-base-1.0",verbose=False)

from rest_framework.permissions import IsAuthenticated
import os

# try:
#     obj=openAiConfig.objects.first()
#     if obj.server_on:
#
#         client = OpenAI(api_key=obj.api_key)
#         print(client.api_key,obj.api_key)
#
#
# except Exception as e:
#     print(e)
#     obj=False
#     client = False

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
            if client:
                re = client.predict(
                    param_0=text,
                    api_name="/predict"
                )

                if re:
                    gen_obj=generationsHistory.objects.create(text=text,user=self.request.user,img_url=re)
                    gen_obj.img.save(
                        os.path.basename(re),
                        File(open(re, 'rb'))
                    )
                    return Response(generationsHistorySerializer(gen_obj,context={'request':request}).data,status=200)
                else:
                    return self.error_message('model error',status.HTTP_400_BAD_REQUEST)
            else:
                return self.error_message('server Ai model is not working',status.HTTP_400_BAD_REQUEST)
        return self.error_message('test is missing',status.HTTP_400_BAD_REQUEST)



