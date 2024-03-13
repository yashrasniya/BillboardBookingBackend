from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import razorpay
from billboard.models import BillBoard
from accounts.models import *
from accounts.views import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from accounts.models import User
import django
from datetime import date
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

# import razorpay
try:
    RGD = razorpay_gateway_detail.objects.all()[0]
    # client = razorpay.Client(auth=("rzp_test_u01RD7HTlF1ysu", "oJclH13vmmj5evdT5HeKXrOG"))pxcGYJTKy2rc2fSIoLTlvrJA
    client = razorpay.Client(auth=(RGD.razorpay_id, RGD.razorpay_SECRET))
except (django.db.utils.ProgrammingError, razorpay_gateway_detail.DoesNotExist, django.db.utils.OperationalError,
        IndexError) as e:
    print(e)


# Create your views here.
def fetching_link(price, reference_id, user_name, user_contact, user_email):
    print(price, reference_id, user_name, user_contact, user_email)
    p = client.payment_link.create({
        "amount": price,
        "currency": "INR",

        "reference_id": reference_id,
        "callback_url": RGD.call_back_url,
        "description": "Payment for policy no #23456",
        "customer": {
            "name": user_name,
            "contact": user_contact,
            "email": user_email
        },
        "notify": {
            "sms": False,
            "email": False
        },
        "reminder_enable": True,
        "options": {
            "checkout": {
                "theme": {
                    "hide_topbar": True
                }
            }
        }
    })
    print(p['short_url'])
    return {'link': p['short_url']}


class create_payment_link(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, bill_board_id):
        user_obj = request.user


        discount = 0
        user_name = request.user.name()
        user_contact = request.user.mobile_number
        user_email = request.user.email
        try:
            int(user_contact)
        except ValueError as e:
            user_contact = '9888888888'
        try:
            bill_board_obj = BillBoard.objects.filter(id=bill_board_id)
            if not bill_board_obj:
                return Response({'message':'billboard id not found'})
            bill_board_obj=bill_board_obj.first()
            price = bill_board_obj.price

            obj = Create_payment_link.objects.create(amount=str(price),
                                                     user=user_obj,
                                                     billboard=bill_board_obj
                                                     )
            obj.save()
            print(obj.id, price)
            d = fetching_link(int(price*100),
                              f'NINE{obj.id}',
                              user_name, user_contact, user_email)

            data = {'status': 200}
            data.update(d)

            return Response(data, status.HTTP_200_OK)


        except Exception as e:
            return HttpResponse({'status': '404', 'message': 'Not found', 'error': f'{e}'},
                                status=status.HTTP_404_NOT_FOUND)



class verify_payment(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        subject = False
        mentors = False
        payment_id = request.GET['razorpay_payment_id']
        payment_linkID = request.GET['razorpay_payment_link_id']
        payment_link_reference_id = request.GET['razorpay_payment_link_reference_id']
        payment_link_status = request.GET['razorpay_payment_link_status']
        signature = request.GET['razorpay_signature']
        try:

            obj = Create_payment_link.objects.filter(id=payment_link_reference_id[4:])
            obj_2 = Create_payment_link.objects.get(id=payment_link_reference_id[4:])
        except IndexError as e:
            print(e)
            obj = Create_payment_link.objects.filter(id=payment_link_reference_id)
        if obj:
            if get_verify(payment_link_id=payment_linkID,
                          payment_link_reference_id=payment_link_reference_id,
                          payment_link_status=payment_link_status,
                          razorpay_payment_id=payment_id,
                          razorpay_signature=signature):
                obj.update(payment_link_id=payment_linkID,
                           payment_link_status=payment_link_status,
                           reference_id=payment_link_reference_id,
                           razorpay_payment_id=payment_id,
                           razorpay_signature=signature

                           )
                print(obj[0].reference_id,obj)
                user_obj = User.objects.get(username=obj[0].user.username)

                obj_2.status = '0'
                obj_2.save()
                user_obj.save()
                data = {'status': 200}
                data.update(request.GET)
                return Response(data, status.HTTP_200_OK)

            else:
                return Response({'status': '400', 'message': 'get is not allowed', 'error': f''},
                                status.HTTP_400_BAD_REQUEST)
        return Response({'status': '404', 'message': 'get is not allowed', 'error': f''},
                        status.HTTP_404_NOT_FOUND)


def get_verify(payment_link_id, payment_link_reference_id,
               payment_link_status, razorpay_payment_id, razorpay_signature):
    o = False
    try:

        o = client.utility.verify_payment_link_signature({
            'payment_link_id': payment_link_id,
            'payment_link_reference_id': payment_link_reference_id,
            'payment_link_status': payment_link_status,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
    except razorpay.errors.SignatureVerificationError as e:
        print(e)

    print(o)
    return o





class TransactionHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(Create_payment_link.objects.filter(user=request.user,status=0).values())
